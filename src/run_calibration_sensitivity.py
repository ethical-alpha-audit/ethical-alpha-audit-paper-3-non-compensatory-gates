#!/usr/bin/env python3
"""
Calibration Sensitivity Analyses

Tests robustness of primary findings to alternative portfolio composition
and unsafe probability parameters.

  3.1 Portfolio composition: 10/90 through 50/50 high-risk/standard-risk
  3.2 Unsafe probability: ±30% of default values

Usage:
    python run_calibration_sensitivity.py
    python run_calibration_sensitivity.py --analysis portfolio
    python run_calibration_sensitivity.py --analysis unsafe-prob
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from run_simulation import (
    SimConfig, load_config, simulate_portfolio, GATES, clip01,
    decide_noncomp_gates, decide_weighted_composite, decide_permissive,
    compute_metrics, bootstrap_ci, set_threshold_to_match_rate,
    C_GATE, C_COMP_MEAN, C_PERMISSIVE, _style_ax,
)


def _make_config(base: SimConfig, **overrides) -> SimConfig:
    """Create a modified SimConfig preserving non-serialisable fields."""
    d = asdict(base)
    d.update(overrides)
    d["override_disallowed_gates"] = tuple(d["override_disallowed_gates"])
    d["unsafe_gate_profile"] = {k: tuple(v) for k, v in d["unsafe_gate_profile"].items()}
    return SimConfig(**d)


def run_single(cfg: SimConfig, label: str) -> dict:
    """Run a single simulation variant and return metrics."""
    df = simulate_portfolio(cfg)
    df = decide_noncomp_gates(df, cfg)
    gate_rate = float(df["deploy_gate"].mean())

    if gate_rate <= 0 or gate_rate >= 1:
        return {"label": label, "error": f"gate_rate={gate_rate:.3f}"}

    weights = cfg.composite_weights
    tmp = decide_weighted_composite(df, weights, threshold=0.0, missing_mode="mean")
    scores = tmp["composite_score_mean"].to_numpy()

    thr_moderate = set_threshold_to_match_rate(scores, min(gate_rate * 2.2, 0.85))
    thr_matched = set_threshold_to_match_rate(scores, gate_rate)

    df = decide_weighted_composite(df, weights, threshold=thr_moderate, missing_mode="mean")
    df = decide_weighted_composite(df, weights, threshold=thr_matched,
                                   missing_mode="mean", col_suffix="matched")
    df = decide_permissive(df, cfg)

    result = {"label": label}
    for method, col in [("Gates", "deploy_gate"),
                        ("Composite (moderate)", "deploy_composite_mean"),
                        ("Composite (matched)", "deploy_composite_matched"),
                        ("Permissive", "deploy_permissive")]:
        m = compute_metrics(df, col)
        result[f"{method}_deploy_rate"] = m["deployment_rate"]
        result[f"{method}_unsafe_rate"] = m["unsafe_deployment_rate"]
        result[f"{method}_contam_rate"] = m["unsafe_among_deployed"]

        # Bootstrap CI for gates and composite moderate
        if method in ("Gates", "Composite (moderate)"):
            lo, hi = bootstrap_ci(df, col, "unsafe_deployment_rate",
                                  n_boot=cfg.n_bootstrap, seed=cfg.seed + 42)
            result[f"{method}_unsafe_ci_lo"] = lo
            result[f"{method}_unsafe_ci_hi"] = hi

    return result


# ── Portfolio composition sensitivity ────────────────────────────────────────

PORTFOLIO_SPLITS = [
    (0.10, "10% high / 90% std"),
    (0.20, "20% high / 80% std"),
    (0.30, "30% high / 70% std (reference)"),
    (0.40, "40% high / 60% std"),
    (0.50, "50% high / 50% std"),
]

def run_portfolio_sensitivity(base_cfg: SimConfig, out_dir: Path) -> pd.DataFrame:
    print("\nPortfolio Composition Sensitivity")
    print("=" * 60)
    results = []
    for p_high, label in PORTFOLIO_SPLITS:
        cfg = _make_config(base_cfg, p_high_risk=p_high)
        r = run_single(cfg, label)
        results.append(r)
        if "error" not in r:
            print(f"  {label:<35s}  Gates unsafe={r['Gates_unsafe_rate']:.4f}  "
                  f"Comp(mod) unsafe={r['Composite (moderate)_unsafe_rate']:.4f}")
        else:
            print(f"  {label}: {r['error']}")

    df = pd.DataFrame(results)
    df.to_csv(out_dir / "calibration_portfolio.csv", index=False)
    return df


# ── Unsafe probability sensitivity ──────────────────────────────────────────

UNSAFE_PROBS = [
    (0.20, 0.08, "P(unsafe)=0.20/0.08 (lower)"),
    (0.25, 0.10, "P(unsafe)=0.25/0.10 (conservative)"),
    (0.35, 0.15, "P(unsafe)=0.35/0.15 (reference)"),
    (0.45, 0.20, "P(unsafe)=0.45/0.20 (higher)"),
    (0.50, 0.25, "P(unsafe)=0.50/0.25 (stress test)"),
]

def run_unsafe_prob_sensitivity(base_cfg: SimConfig, out_dir: Path) -> pd.DataFrame:
    print("\nUnsafe Probability Sensitivity")
    print("=" * 60)
    results = []
    for p_high, p_std, label in UNSAFE_PROBS:
        cfg = _make_config(base_cfg, p_unsafe_high=p_high, p_unsafe_standard=p_std)
        r = run_single(cfg, label)
        results.append(r)
        if "error" not in r:
            print(f"  {label:<40s}  Gates unsafe={r['Gates_unsafe_rate']:.4f}  "
                  f"Comp(mod) unsafe={r['Composite (moderate)_unsafe_rate']:.4f}")
        else:
            print(f"  {label}: {r['error']}")

    df = pd.DataFrame(results)
    df.to_csv(out_dir / "calibration_unsafe_prob.csv", index=False)
    return df


# ── Figures ──────────────────────────────────────────────────────────────────

def plot_sensitivity(df: pd.DataFrame, x_col: str, x_label: str,
                     title: str, filename: str, out_dir: Path) -> None:
    """Plot gates vs composite (moderate) unsafe rate across a parameter."""
    if "error" in df.columns:
        df = df[df["error"].isna() | (df["error"] == "")]

    fig, ax = plt.subplots(figsize=(8, 5))

    x_vals = range(len(df))
    labels = df["label"].tolist()

    gates_rates = df["Gates_unsafe_rate"].tolist()
    comp_rates = df["Composite (moderate)_unsafe_rate"].tolist()
    perm_rates = df["Permissive_unsafe_rate"].tolist()

    w = 0.25
    x_arr = np.arange(len(df))

    ax.bar(x_arr - w, gates_rates, w, label="Gates", color=C_GATE, edgecolor="white")
    ax.bar(x_arr, comp_rates, w, label="Composite (moderate)", color=C_COMP_MEAN, edgecolor="white")
    ax.bar(x_arr + w, perm_rates, w, label="Permissive", color=C_PERMISSIVE, edgecolor="white")

    # Value labels
    for i in range(len(df)):
        for offset, vals in [(-w, gates_rates), (0, comp_rates), (w, perm_rates)]:
            ax.text(i + offset, vals[i] + 0.001, f"{vals[i]:.3f}",
                    ha="center", va="bottom", fontsize=7, rotation=45)

    ax.set_xticks(x_arr)
    ax.set_xticklabels(labels, fontsize=8, rotation=15, ha="right")
    ax.set_ylabel("Unsafe deployment rate", fontsize=11)
    ax.set_title(title, fontsize=12, pad=12)
    ax.legend(frameon=False, fontsize=9)
    _style_ax(ax)
    ax.set_ylim(bottom=0)
    plt.tight_layout()
    fig.savefig(out_dir / f"{filename}.png", dpi=300, bbox_inches="tight")
    fig.savefig(out_dir / f"{filename}.pdf", bbox_inches="tight")
    plt.close(fig)


# ── Main ─────────────────────────────────────────────────────────────────────

def main(argv=None):
    parser = argparse.ArgumentParser(description="Calibration sensitivity analyses")
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--analysis", type=str, default=None,
                        choices=["portfolio", "unsafe-prob"],
                        help="Run a single analysis (default: both)")
    parser.add_argument("--output-dir", type=str, default=None)
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    out_dir = Path(args.output_dir) if args.output_dir else Path(__file__).parent / "outputs" / "calibration"
    out_dir.mkdir(parents=True, exist_ok=True)

    analyses = [args.analysis] if args.analysis else ["portfolio", "unsafe-prob"]
    all_results = {}

    if "portfolio" in analyses:
        df_port = run_portfolio_sensitivity(cfg, out_dir)
        all_results["portfolio"] = df_port
        plot_sensitivity(df_port, "label", "Portfolio Composition",
                        "Portfolio Composition Sensitivity",
                        "fig_portfolio_sensitivity", out_dir)

    if "unsafe-prob" in analyses:
        df_prob = run_unsafe_prob_sensitivity(cfg, out_dir)
        all_results["unsafe_prob"] = df_prob
        plot_sensitivity(df_prob, "label", "Unsafe Probability",
                        "Unsafe Probability Sensitivity",
                        "fig_unsafe_prob_sensitivity", out_dir)

    # Combined summary
    print(f"\n{'='*72}")
    print("CALIBRATION SENSITIVITY SUMMARY")
    print(f"{'='*72}")
    for key, df in all_results.items():
        print(f"\n--- {key} ---")
        print(df.to_string(index=False))

    print(f"\nOutputs: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
