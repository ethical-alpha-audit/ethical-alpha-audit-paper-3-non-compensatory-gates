#!/usr/bin/env python3
"""
Verification Simulations for Analytical Scope Conditions

Implements the three verification simulations specified in the
Supplementary Simulation Specification:
  A. Uniform failure
  B. Random failure
  C. Partial heterogeneity

Each simulation uses the same portfolio generation and decision rule
logic as the primary simulation, with only the evidence generation
model altered.

Usage:
    python run_verification.py                     # all three scenarios
    python run_verification.py --scenario uniform   # single scenario
    python run_verification.py --output-dir ./outputs/verification
"""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from run_simulation import (
    SimConfig, load_config, GATES, clip01,
    decide_noncomp_gates, decide_weighted_composite, decide_permissive,
    compute_metrics, bootstrap_ci, set_threshold_to_match_rate,
    C_GATE, C_COMP_MEAN, C_PERMISSIVE, _style_ax,
)


# ── Evidence models ──────────────────────────────────────────────────────────

def simulate_uniform_failure(cfg: SimConfig) -> pd.DataFrame:
    """Uniform failure: unsafe tools fail equally across ALL five domains."""
    rng = np.random.default_rng(cfg.seed)
    n = cfg.n_tools

    is_high = rng.random(n) < cfg.p_high_risk
    risk_tier = np.where(is_high, "high", "standard")
    p_unsafe = np.where(is_high, cfg.p_unsafe_high, cfg.p_unsafe_standard)
    unsafe_true = rng.random(n) < p_unsafe
    safe_true = ~unsafe_true
    maturity = rng.normal(0.0, cfg.maturity_effect_sd, n)

    rows = {
        "tool_id": [f"T{i:04d}" for i in range(n)],
        "risk_tier": risk_tier,
        "unsafe_true": unsafe_true.astype(int),
    }

    for g in GATES:
        latent = np.empty(n, dtype=float)

        # Safe tools: same as primary model
        n_safe = int(safe_true.sum())
        if n_safe > 0:
            latent[safe_true] = rng.beta(cfg.safe_beta_a, cfg.safe_beta_b, n_safe)

        # Unsafe tools: UNIFORM failure — same low score across all domains
        n_unsafe = int(unsafe_true.sum())
        if n_unsafe > 0:
            # Use the base unsafe distribution (no gate-specific shifts)
            latent[unsafe_true] = rng.beta(cfg.unsafe_beta_a, cfg.unsafe_beta_b, n_unsafe)

        # Maturity effect on process-oriented gates
        if g in ("G3_Documentation", "G4_Accountability", "G5_Monitoring"):
            latent = latent + maturity

        latent = clip01(latent)

        # Missingness
        p_miss_s = cfg.p_missing_safe.get(g, 0.0)
        p_miss_u = cfg.p_missing_unsafe.get(g, 0.0)
        p_miss = np.where(safe_true, p_miss_s, p_miss_u)
        missing = rng.random(n) < p_miss

        obs = latent + rng.normal(0.0, cfg.obs_noise_sd, n)
        obs = clip01(obs)
        obs[missing] = np.nan

        rows[f"{g}_latent"] = latent
        rows[f"{g}_missing"] = missing.astype(int)
        rows[f"{g}_obs"] = obs

    return pd.DataFrame(rows)


def simulate_random_failure(cfg: SimConfig) -> pd.DataFrame:
    """Random failure: unsafe tools fail in 2-4 randomly chosen domains."""
    rng = np.random.default_rng(cfg.seed)
    n = cfg.n_tools

    is_high = rng.random(n) < cfg.p_high_risk
    risk_tier = np.where(is_high, "high", "standard")
    p_unsafe = np.where(is_high, cfg.p_unsafe_high, cfg.p_unsafe_standard)
    unsafe_true = rng.random(n) < p_unsafe
    safe_true = ~unsafe_true
    maturity = rng.normal(0.0, cfg.maturity_effect_sd, n)

    # Pre-assign failing domains per unsafe tool
    n_unsafe = int(unsafe_true.sum())
    failing_domains = []
    for _ in range(n_unsafe):
        n_fail = rng.integers(2, 5)  # 2, 3, or 4 domains fail
        fail_indices = rng.choice(5, size=n_fail, replace=False)
        failing_domains.append(set(fail_indices))

    rows = {
        "tool_id": [f"T{i:04d}" for i in range(n)],
        "risk_tier": risk_tier,
        "unsafe_true": unsafe_true.astype(int),
    }

    unsafe_counter = 0
    unsafe_indices = np.where(unsafe_true)[0]

    for gi, g in enumerate(GATES):
        latent = np.empty(n, dtype=float)

        # Safe tools: same as primary model
        n_safe = int(safe_true.sum())
        if n_safe > 0:
            latent[safe_true] = rng.beta(cfg.safe_beta_a, cfg.safe_beta_b, n_safe)

        # Unsafe tools: fail only in randomly assigned domains
        for j, idx in enumerate(unsafe_indices):
            if gi in failing_domains[j]:
                # Failing domain: draw from below-threshold distribution
                latent[idx] = rng.beta(cfg.unsafe_beta_a, cfg.unsafe_beta_b)
            else:
                # Passing domain: draw from safe-tool distribution
                latent[idx] = rng.beta(cfg.safe_beta_a, cfg.safe_beta_b)

        if g in ("G3_Documentation", "G4_Accountability", "G5_Monitoring"):
            latent = latent + maturity

        latent = clip01(latent)

        p_miss_s = cfg.p_missing_safe.get(g, 0.0)
        p_miss_u = cfg.p_missing_unsafe.get(g, 0.0)
        p_miss = np.where(safe_true, p_miss_s, p_miss_u)
        missing = rng.random(n) < p_miss

        obs = latent + rng.normal(0.0, cfg.obs_noise_sd, n)
        obs = clip01(obs)
        obs[missing] = np.nan

        rows[f"{g}_latent"] = latent
        rows[f"{g}_missing"] = missing.astype(int)
        rows[f"{g}_obs"] = obs

    return pd.DataFrame(rows)


def simulate_partial_heterogeneity(cfg: SimConfig) -> pd.DataFrame:
    """Partial heterogeneity: unsafe tools fail in 3 latent domains
    (equity, accountability, monitoring) but not in visible domains
    (safety, documentation)."""
    rng = np.random.default_rng(cfg.seed)
    n = cfg.n_tools

    is_high = rng.random(n) < cfg.p_high_risk
    risk_tier = np.where(is_high, "high", "standard")
    p_unsafe = np.where(is_high, cfg.p_unsafe_high, cfg.p_unsafe_standard)
    unsafe_true = rng.random(n) < p_unsafe
    safe_true = ~unsafe_true
    maturity = rng.normal(0.0, cfg.maturity_effect_sd, n)

    # Latent domains that fail for unsafe tools
    failing_gates = {"G2_Equity", "G4_Accountability", "G5_Monitoring"}

    rows = {
        "tool_id": [f"T{i:04d}" for i in range(n)],
        "risk_tier": risk_tier,
        "unsafe_true": unsafe_true.astype(int),
    }

    for g in GATES:
        latent = np.empty(n, dtype=float)

        n_safe = int(safe_true.sum())
        if n_safe > 0:
            latent[safe_true] = rng.beta(cfg.safe_beta_a, cfg.safe_beta_b, n_safe)

        n_unsafe = int(unsafe_true.sum())
        if n_unsafe > 0:
            if g in failing_gates:
                # Failing domain: draw from base unsafe distribution
                latent[unsafe_true] = rng.beta(cfg.unsafe_beta_a, cfg.unsafe_beta_b, n_unsafe)
            else:
                # Visible domain: draw from safe-tool distribution (looks good)
                latent[unsafe_true] = rng.beta(cfg.safe_beta_a, cfg.safe_beta_b, n_unsafe)

        if g in ("G3_Documentation", "G4_Accountability", "G5_Monitoring"):
            latent = latent + maturity

        latent = clip01(latent)

        p_miss_s = cfg.p_missing_safe.get(g, 0.0)
        p_miss_u = cfg.p_missing_unsafe.get(g, 0.0)
        p_miss = np.where(safe_true, p_miss_s, p_miss_u)
        missing = rng.random(n) < p_miss

        obs = latent + rng.normal(0.0, cfg.obs_noise_sd, n)
        obs = clip01(obs)
        obs[missing] = np.nan

        rows[f"{g}_latent"] = latent
        rows[f"{g}_missing"] = missing.astype(int)
        rows[f"{g}_obs"] = obs

    return pd.DataFrame(rows)


# ── Run all decision rules on a portfolio ────────────────────────────────────

def apply_all_rules(df: pd.DataFrame, cfg: SimConfig) -> dict:
    """Apply gates, composite (moderate & matched), and permissive rules.
    Returns metrics dict."""
    weights = cfg.composite_weights

    df = decide_noncomp_gates(df, cfg)
    gate_deploy_rate = float(df["deploy_gate"].mean())

    if gate_deploy_rate <= 0 or gate_deploy_rate >= 1:
        # Edge case: return NaN metrics
        return {"error": f"gate_deploy_rate={gate_deploy_rate}"}

    # Composite (mean imputation)
    tmp = decide_weighted_composite(df, weights, threshold=0.0, missing_mode="mean")
    scores = tmp["composite_score_mean"].to_numpy()

    thr_matched = set_threshold_to_match_rate(scores, gate_deploy_rate)
    thr_moderate = set_threshold_to_match_rate(scores, min(gate_deploy_rate * 2.2, 0.85))

    df = decide_weighted_composite(df, weights, threshold=thr_matched,
                                   missing_mode="mean", col_suffix="matched")
    df = decide_weighted_composite(df, weights, threshold=thr_moderate,
                                   missing_mode="mean")
    df = decide_permissive(df, cfg)

    results = {
        "Gates": compute_metrics(df, "deploy_gate"),
        "Composite (matched)": compute_metrics(df, "deploy_composite_matched"),
        "Composite (moderate)": compute_metrics(df, "deploy_composite_mean"),
        "Permissive": compute_metrics(df, "deploy_permissive"),
    }

    # Bootstrap CIs for key metrics
    for label, col in [("Gates", "deploy_gate"),
                       ("Composite (moderate)", "deploy_composite_mean"),
                       ("Permissive", "deploy_permissive")]:
        for mk in ["unsafe_deployment_rate", "unsafe_among_deployed"]:
            lo, hi = bootstrap_ci(df, col, mk, n_boot=cfg.n_bootstrap, seed=cfg.seed + 42)
            results[label][f"{mk}_ci"] = (lo, hi)

    results["gate_deploy_rate"] = gate_deploy_rate
    results["thr_matched"] = thr_matched
    results["thr_moderate"] = thr_moderate

    return results


# ── Main ─────────────────────────────────────────────────────────────────────

SCENARIOS = {
    "uniform": ("Uniform Failure", simulate_uniform_failure),
    "random": ("Random Failure", simulate_random_failure),
    "partial": ("Partial Heterogeneity", simulate_partial_heterogeneity),
}


def run_scenario(name: str, cfg: SimConfig, out_dir: Path) -> dict:
    label, sim_fn = SCENARIOS[name]
    print(f"\n{'='*60}")
    print(f"Verification Simulation: {label}")
    print(f"{'='*60}")

    df = sim_fn(cfg)
    results = apply_all_rules(df, cfg)

    if "error" in results:
        print(f"  ERROR: {results['error']}")
        return results

    # Print headline
    print(f"\n  {'Method':<25s} {'Deploy%':>8s} {'Unsafe%':>8s} {'Contam%':>8s}")
    print(f"  {'-'*51}")
    for method in ["Gates", "Composite (matched)", "Composite (moderate)", "Permissive"]:
        m = results[method]
        ci_str = ""
        if f"unsafe_deployment_rate_ci" in m:
            lo, hi = m["unsafe_deployment_rate_ci"]
            ci_str = f"  [{lo:.3f}, {hi:.3f}]"
        print(f"  {method:<25s} {m['deployment_rate']:>8.3f} "
              f"{m['unsafe_deployment_rate']:>8.3f} "
              f"{m['unsafe_among_deployed']:>8.3f}{ci_str}")

    # Save CSV
    df.to_csv(out_dir / f"verification_{name}_portfolio.csv", index=False)

    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description="Verification simulations")
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--scenario", type=str, default=None,
                        choices=list(SCENARIOS.keys()),
                        help="Run a single scenario (default: all)")
    parser.add_argument("--output-dir", type=str, default=None)
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    out_dir = Path(args.output_dir) if args.output_dir else Path(__file__).parent / "outputs" / "verification"
    out_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [args.scenario] if args.scenario else list(SCENARIOS.keys())
    all_results = {}

    for name in scenarios:
        all_results[name] = run_scenario(name, cfg, out_dir)

    # ── Summary table ────────────────────────────────────────────────────
    print(f"\n\n{'='*72}")
    print("VERIFICATION SIMULATION SUMMARY TABLE")
    print(f"{'='*72}")
    
    rows = []
    for name in scenarios:
        r = all_results[name]
        if "error" in r:
            continue
        label = SCENARIOS[name][0]
        for method in ["Gates", "Composite (moderate)", "Composite (matched)", "Permissive"]:
            m = r[method]
            ci_lo, ci_hi = m.get("unsafe_deployment_rate_ci", (float("nan"), float("nan")))
            rows.append({
                "Scenario": label,
                "Decision Rule": method,
                "Deployment Rate": m["deployment_rate"],
                "Unsafe Deployment Rate": m["unsafe_deployment_rate"],
                "Unsafe Deploy 95% CI Low": ci_lo,
                "Unsafe Deploy 95% CI High": ci_hi,
                "Contamination Rate": m["unsafe_among_deployed"],
            })

    summary_df = pd.DataFrame(rows)
    summary_df.to_csv(out_dir / "verification_summary.csv", index=False)
    print(summary_df.to_string(index=False))

    # Save JSON
    json_results = {}
    for name, r in all_results.items():
        if "error" in r:
            json_results[name] = r
            continue
        json_results[name] = {}
        for method in ["Gates", "Composite (matched)", "Composite (moderate)", "Permissive"]:
            m = r[method]
            json_results[name][method] = {
                k: v if not isinstance(v, tuple) else list(v)
                for k, v in m.items()
            }
        json_results[name]["gate_deploy_rate"] = r.get("gate_deploy_rate")

    (out_dir / "verification_results.json").write_text(
        json.dumps(json_results, indent=2, default=str), encoding="utf-8"
    )

    # ── Figure: comparative bar chart ────────────────────────────────────
    if len(scenarios) >= 2:
        fig, axes = plt.subplots(1, len(scenarios), figsize=(5 * len(scenarios), 4.5),
                                  sharey=True)
        if len(scenarios) == 1:
            axes = [axes]

        for ax, name in zip(axes, scenarios):
            r = all_results[name]
            if "error" in r:
                continue
            methods = ["Gates", "Composite\n(moderate)", "Composite\n(matched)", "Permissive"]
            keys = ["Gates", "Composite (moderate)", "Composite (matched)", "Permissive"]
            colors = [C_GATE, C_COMP_MEAN, "#67001F", C_PERMISSIVE]
            rates = [r[k]["unsafe_deployment_rate"] for k in keys]

            bars = ax.bar(methods, rates, color=colors, edgecolor="white")
            for bar, val in zip(bars, rates):
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.001,
                        f"{val:.3f}", ha="center", va="bottom", fontsize=8)

            ax.set_title(SCENARIOS[name][0], fontsize=11)
            ax.set_ylabel("Unsafe deployment rate" if name == scenarios[0] else "")
            _style_ax(ax)
            ax.set_ylim(bottom=0)
            ax.tick_params(axis="x", labelsize=8)

        plt.suptitle("Verification Simulations: Unsafe Deployment Rate by Scenario",
                      fontsize=12, y=1.02)
        plt.tight_layout()
        fig.savefig(out_dir / "fig_verification_comparison.png", dpi=300, bbox_inches="tight")
        fig.savefig(out_dir / "fig_verification_comparison.pdf", bbox_inches="tight")
        plt.close(fig)

    print(f"\nOutputs: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
