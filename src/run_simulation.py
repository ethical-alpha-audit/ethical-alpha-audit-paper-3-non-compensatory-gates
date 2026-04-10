#!/usr/bin/env python3
"""
Operationalizing Non-Compensatory Governance Gates:
A Simulation Study of Clinical AI Deployment Decisions

Reference implementation accompanying:
  Brown W. Non-compensatory governance gates for clinical artificial
  intelligence deployment. JMIR Med Inform. Under review.

Produces paper-ready figures, tables, and metrics in ./outputs/.
Deterministic seed ensures full reproducibility.

Usage:
    python run_simulation.py                     # default parameters
    python run_simulation.py --config params.json # custom parameters
    python run_simulation.py --seed 42 --n-tools 5000
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ── Constants ────────────────────────────────────────────────────────────────

GATES = [
    "G1_Safety",
    "G2_Equity",
    "G3_Documentation",
    "G4_Accountability",
    "G5_Monitoring",
]

GATE_LABELS = {
    "G1_Safety": "Safety &\nValidation",
    "G2_Equity": "Bias &\nEquity",
    "G3_Documentation": "Documentation &\nTransparency",
    "G4_Accountability": "Accountability &\nDecision Rights",
    "G5_Monitoring": "Monitoring &\nDrift Mgmt",
}

# Colour palette (colourblind-safe, print-friendly)
C_GATE = "#2166AC"
C_COMP_MEAN = "#B2182B"
C_COMP_ZERO = "#EF8A62"
C_PERMISSIVE = "#999999"
C_SAFE = "#4DAF4A"
C_UNSAFE = "#E41A1C"

# ── Configuration ────────────────────────────────────────────────────────────

@dataclass
class SimConfig:
    """All simulation parameters.  Serialisable to/from JSON."""

    n_tools: int = 1000
    seed: int = 20260304
    n_bootstrap: int = 1000

    # Risk tiers
    p_high_risk: float = 0.30

    # Ground-truth unsafe probabilities
    p_unsafe_standard: float = 0.15
    p_unsafe_high: float = 0.35

    # ── Evidence generation ──────────────────────────────────────────────
    # Safe tools: strong evidence (Beta mean ≈ 0.71)
    safe_beta_a: float = 5.0
    safe_beta_b: float = 2.0

    # Unsafe tools: moderate evidence overall (Beta mean ≈ 0.50)
    unsafe_beta_a: float = 4.0
    unsafe_beta_b: float = 4.0

    # KEY MECHANISM: unsafe tools have *heterogeneous* gate profiles.
    # Some gates score well (creating compensation opportunities for
    # composite scoring), while others score poorly (caught by gates).
    # Dict maps gate → (alpha_shift, beta_shift) ADDED to the base
    # unsafe beta params.
    unsafe_gate_profile: Dict[str, Tuple[float, float]] = field(
        default_factory=lambda: {
            # Safety often looks strong (vendor-reported metrics)
            "G1_Safety": (3.0, -2.0),
            # Equity is systematically weak (no subgroup evaluation)
            "G2_Equity": (-2.0, 2.0),
            # Documentation can be dressed up (glossy model cards)
            "G3_Documentation": (2.0, -1.0),
            # Accountability moderately weak
            "G4_Accountability": (-1.0, 1.0),
            # Monitoring almost always absent for unsafe tools
            "G5_Monitoring": (-2.5, 3.0),
        }
    )

    # Measurement noise
    obs_noise_sd: float = 0.06

    # Correlated organisational maturity effect
    maturity_effect_sd: float = 0.08

    # ── Missingness ──────────────────────────────────────────────────────
    p_missing_safe: Dict[str, float] = field(
        default_factory=lambda: {
            "G1_Safety": 0.03, "G2_Equity": 0.05,
            "G3_Documentation": 0.03, "G4_Accountability": 0.04,
            "G5_Monitoring": 0.04,
        }
    )
    p_missing_unsafe: Dict[str, float] = field(
        default_factory=lambda: {
            "G1_Safety": 0.06, "G2_Equity": 0.18,
            "G3_Documentation": 0.08, "G4_Accountability": 0.10,
            "G5_Monitoring": 0.20,
        }
    )

    # ── Gate thresholds (risk-tiered) ────────────────────────────────────
    thresholds_standard: Dict[str, float] = field(
        default_factory=lambda: {
            "G1_Safety": 0.55, "G2_Equity": 0.50,
            "G3_Documentation": 0.50, "G4_Accountability": 0.50,
            "G5_Monitoring": 0.50,
        }
    )
    thresholds_high: Dict[str, float] = field(
        default_factory=lambda: {
            "G1_Safety": 0.65, "G2_Equity": 0.60,
            "G3_Documentation": 0.60, "G4_Accountability": 0.60,
            "G5_Monitoring": 0.60,
        }
    )

    # ── Override ─────────────────────────────────────────────────────────
    allow_override: bool = True
    override_prob: float = 0.10
    override_max_failed_gates: int = 1
    override_disallowed_gates: Tuple[str, ...] = ("G1_Safety", "G5_Monitoring")

    # ── Composite weights ────────────────────────────────────────────────
    composite_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "G1_Safety": 0.30, "G2_Equity": 0.15,
            "G3_Documentation": 0.15, "G4_Accountability": 0.15,
            "G5_Monitoring": 0.25,
        }
    )

    # ── Permissive baseline ──────────────────────────────────────────────
    permissive_min_gates_passed: int = 3  # deploy if ≥3 of 5 gates pass


def load_config(path: Optional[str] = None) -> SimConfig:
    """Load config from JSON, falling back to defaults."""
    if path is None:
        return SimConfig()
    with open(path) as f:
        d = json.load(f)
    # Convert tuple fields
    if "override_disallowed_gates" in d:
        d["override_disallowed_gates"] = tuple(d["override_disallowed_gates"])
    if "unsafe_gate_profile" in d:
        d["unsafe_gate_profile"] = {
            k: tuple(v) for k, v in d["unsafe_gate_profile"].items()
        }
    return SimConfig(**d)


# ── Utilities ────────────────────────────────────────────────────────────────

def clip01(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0.0, 1.0)


# ── Portfolio simulation ─────────────────────────────────────────────────────

def simulate_portfolio(cfg: SimConfig) -> pd.DataFrame:
    """Generate a portfolio of simulated clinical AI tools with gate evidence."""
    rng = np.random.default_rng(cfg.seed)
    n = cfg.n_tools

    # Risk tiers
    is_high = rng.random(n) < cfg.p_high_risk
    risk_tier = np.where(is_high, "high", "standard")

    # Ground truth
    p_unsafe = np.where(is_high, cfg.p_unsafe_high, cfg.p_unsafe_standard)
    unsafe_true = rng.random(n) < p_unsafe
    safe_true = ~unsafe_true

    # Organisational maturity (correlated across doc/accountability/monitoring)
    maturity = rng.normal(0.0, cfg.maturity_effect_sd, n)

    rows = {
        "tool_id": [f"T{i:04d}" for i in range(n)],
        "risk_tier": risk_tier,
        "unsafe_true": unsafe_true.astype(int),
    }

    for g in GATES:
        latent = np.empty(n, dtype=float)

        # Safe tools: draw from base safe distribution
        n_safe = int(safe_true.sum())
        if n_safe > 0:
            latent[safe_true] = rng.beta(cfg.safe_beta_a, cfg.safe_beta_b, n_safe)

        # Unsafe tools: heterogeneous gate profiles (the key mechanism)
        n_unsafe = int(unsafe_true.sum())
        if n_unsafe > 0:
            a_shift, b_shift = cfg.unsafe_gate_profile.get(g, (0.0, 0.0))
            a = max(cfg.unsafe_beta_a + a_shift, 0.5)
            b = max(cfg.unsafe_beta_b + b_shift, 0.5)
            latent[unsafe_true] = rng.beta(a, b, n_unsafe)

        # Maturity effect on process-oriented gates
        if g in ("G3_Documentation", "G4_Accountability", "G5_Monitoring"):
            latent = latent + maturity

        latent = clip01(latent)

        # Missingness (differential by safety state)
        p_miss_s = cfg.p_missing_safe.get(g, 0.0)
        p_miss_u = cfg.p_missing_unsafe.get(g, 0.0)
        p_miss = np.where(safe_true, p_miss_s, p_miss_u)
        missing = rng.random(n) < p_miss

        # Observed evidence = latent + noise
        obs = latent + rng.normal(0.0, cfg.obs_noise_sd, n)
        obs = clip01(obs)
        obs[missing] = np.nan

        rows[f"{g}_latent"] = latent
        rows[f"{g}_missing"] = missing.astype(int)
        rows[f"{g}_obs"] = obs

    return pd.DataFrame(rows)


# ── Decision rules ───────────────────────────────────────────────────────────

def decide_noncomp_gates(df: pd.DataFrame, cfg: SimConfig) -> pd.DataFrame:
    """Non-compensatory gate rule: deploy only if ALL gates pass."""
    out = df.copy()
    n = len(out)

    tiers = out["risk_tier"].to_numpy()
    fail_counts = np.zeros(n, dtype=int)
    failed_lists: List[List[str]] = [[] for _ in range(n)]

    for i in range(n):
        thr = cfg.thresholds_high if tiers[i] == "high" else cfg.thresholds_standard
        for g in GATES:
            obs = out.at[i, f"{g}_obs"]
            if pd.isna(obs) or float(obs) < float(thr[g]):
                failed_lists[i].append(g)
                fail_counts[i] += 1

    out["failed_gates"] = [",".join(x) if x else "" for x in failed_lists]
    out["n_failed_gates"] = fail_counts

    deploy = fail_counts == 0
    override_used = np.zeros(n, dtype=int)

    if cfg.allow_override:
        rng = np.random.default_rng(cfg.seed + 1)
        eligible = (fail_counts > 0) & (fail_counts <= cfg.override_max_failed_gates)
        for idx in np.where(eligible)[0]:
            if any(g in cfg.override_disallowed_gates for g in failed_lists[idx]):
                eligible[idx] = False
        invoked = eligible & (rng.random(n) < cfg.override_prob)
        deploy = deploy | invoked
        override_used[invoked] = 1

    out["deploy_gate"] = deploy.astype(int)
    out["override_used"] = override_used.astype(int)
    return out


def decide_weighted_composite(
    df: pd.DataFrame,
    weights: Dict[str, float],
    threshold: float,
    missing_mode: str = "mean",
    col_suffix: Optional[str] = None,
) -> pd.DataFrame:
    """Weighted composite score: deploy if aggregate score ≥ threshold."""
    out = df.copy()
    suffix = col_suffix or missing_mode
    obs_mat = np.column_stack([out[f"{g}_obs"].to_numpy(dtype=float) for g in GATES])

    if missing_mode == "mean":
        col_means = np.nanmean(obs_mat, axis=0)
        for j in range(obs_mat.shape[1]):
            mask = np.isnan(obs_mat[:, j])
            obs_mat[mask, j] = col_means[j]
    elif missing_mode == "zero":
        obs_mat = np.nan_to_num(obs_mat, nan=0.0)

    w = np.array([weights[g] for g in GATES], dtype=float)
    score = obs_mat @ w
    out[f"composite_score_{suffix}"] = score
    out[f"deploy_composite_{suffix}"] = (score >= threshold).astype(int)
    return out


def decide_permissive(df: pd.DataFrame, cfg: SimConfig) -> pd.DataFrame:
    """Permissive baseline: deploy if at least K of 5 gates pass."""
    out = df.copy()
    n = len(out)
    tiers = out["risk_tier"].to_numpy()
    pass_counts = np.zeros(n, dtype=int)

    for i in range(n):
        thr = cfg.thresholds_high if tiers[i] == "high" else cfg.thresholds_standard
        for g in GATES:
            obs = out.at[i, f"{g}_obs"]
            if not pd.isna(obs) and float(obs) >= float(thr[g]):
                pass_counts[i] += 1

    out["gates_passed"] = pass_counts
    out["deploy_permissive"] = (pass_counts >= cfg.permissive_min_gates_passed).astype(int)
    return out


# ── Metrics ──────────────────────────────────────────────────────────────────

def compute_metrics(df: pd.DataFrame, deploy_col: str) -> Dict[str, float]:
    deploy = df[deploy_col].to_numpy().astype(bool)
    unsafe = df["unsafe_true"].to_numpy().astype(bool)

    n_deployed = int(deploy.sum())
    n_unsafe_deployed = int((deploy & unsafe).sum())
    n_safe_blocked = int(((~deploy) & (~unsafe)).sum())
    n_safe = int((~unsafe).sum())
    n_unsafe = int(unsafe.sum())

    return {
        "n_tools": int(len(df)),
        "n_deployed": n_deployed,
        "deployment_rate": float(deploy.mean()),
        "n_unsafe_deployed": n_unsafe_deployed,
        "unsafe_deployment_rate": float((deploy & unsafe).mean()),
        "safe_blocked_rate": float(n_safe_blocked / n_safe) if n_safe > 0 else float("nan"),
        "unsafe_among_deployed": float(unsafe[deploy].mean()) if n_deployed > 0 else float("nan"),
        "sensitivity": float(n_unsafe_deployed / n_unsafe) if n_unsafe > 0 else float("nan"),
        "specificity": float(1.0 - n_safe_blocked / n_safe) if n_safe > 0 else float("nan"),
    }


def bootstrap_ci(
    df: pd.DataFrame, deploy_col: str, metric_key: str,
    n_boot: int = 1000, seed: int = 999, alpha: float = 0.05,
) -> Tuple[float, float]:
    """Bootstrap 95 % confidence interval for a given metric."""
    rng = np.random.default_rng(seed)
    n = len(df)
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        sample = df.iloc[idx]
        m = compute_metrics(sample, deploy_col)
        vals.append(m[metric_key])
    lo = float(np.percentile(vals, 100 * alpha / 2))
    hi = float(np.percentile(vals, 100 * (1 - alpha / 2)))
    return lo, hi


def set_threshold_to_match_rate(scores: np.ndarray, target_rate: float) -> float:
    q = min(max(1.0 - target_rate, 0.0), 1.0)
    return float(np.quantile(scores, q))


# ── Sensitivity analysis ────────────────────────────────────────────────────

def sensitivity_over_thresholds(
    df: pd.DataFrame, cfg: SimConfig, weights: Dict[str, float],
    multipliers: np.ndarray,
) -> pd.DataFrame:
    """Vary gate thresholds by a multiplier and compare methods."""
    records = []
    for mult in multipliers:
        # Scale thresholds
        cfg_mod = SimConfig(
            **{
                **{k: v for k, v in asdict(cfg).items()
                   if k not in ("thresholds_standard", "thresholds_high",
                                "unsafe_gate_profile", "override_disallowed_gates",
                                "p_missing_safe", "p_missing_unsafe",
                                "composite_weights")},
                "thresholds_standard": {g: clip01(np.array([v * mult]))[0]
                                        for g, v in cfg.thresholds_standard.items()},
                "thresholds_high": {g: clip01(np.array([v * mult]))[0]
                                    for g, v in cfg.thresholds_high.items()},
                "unsafe_gate_profile": cfg.unsafe_gate_profile,
                "override_disallowed_gates": cfg.override_disallowed_gates,
                "p_missing_safe": cfg.p_missing_safe,
                "p_missing_unsafe": cfg.p_missing_unsafe,
                "composite_weights": cfg.composite_weights,
            }
        )
        df_g = decide_noncomp_gates(df, cfg_mod)

        # Composite calibrated to match gate deployment rate
        target = float(df_g["deploy_gate"].mean())
        if target <= 0 or target >= 1:
            continue

        tmp = decide_weighted_composite(df_g, weights, threshold=0.0, missing_mode="mean")
        thr = set_threshold_to_match_rate(
            tmp["composite_score_mean"].to_numpy(), target
        )
        df_c = decide_weighted_composite(df_g, weights, threshold=thr, missing_mode="mean")

        m_g = compute_metrics(df_c, "deploy_gate")
        m_c = compute_metrics(df_c, "deploy_composite_mean")

        records.append({
            "threshold_multiplier": float(mult),
            "deployment_rate": m_g["deployment_rate"],
            "gate_unsafe_deploy": m_g["unsafe_deployment_rate"],
            "gate_unsafe_among_deployed": m_g["unsafe_among_deployed"],
            "composite_unsafe_deploy": m_c["unsafe_deployment_rate"],
            "composite_unsafe_among_deployed": m_c["unsafe_among_deployed"],
        })

    return pd.DataFrame(records)


# ── Noise robustness analysis ───────────────────────────────────────────────

def noise_robustness(
    cfg: SimConfig, weights: Dict[str, float],
    noise_levels: np.ndarray,
) -> pd.DataFrame:
    """Re-run simulation across varying observation noise levels."""
    records = []
    for noise_sd in noise_levels:
        cfg_mod_dict = asdict(cfg)
        cfg_mod_dict["obs_noise_sd"] = float(noise_sd)
        cfg_mod_dict["override_disallowed_gates"] = tuple(cfg_mod_dict["override_disallowed_gates"])
        cfg_mod_dict["unsafe_gate_profile"] = {
            k: tuple(v) for k, v in cfg_mod_dict["unsafe_gate_profile"].items()
        }
        cfg_mod = SimConfig(**cfg_mod_dict)

        df = simulate_portfolio(cfg_mod)
        df = decide_noncomp_gates(df, cfg_mod)

        target = float(df["deploy_gate"].mean())
        if target <= 0 or target >= 1:
            continue

        tmp = decide_weighted_composite(df, weights, threshold=0.0, missing_mode="mean")
        thr = set_threshold_to_match_rate(
            tmp["composite_score_mean"].to_numpy(), target
        )
        df = decide_weighted_composite(df, weights, threshold=thr, missing_mode="mean")

        m_g = compute_metrics(df, "deploy_gate")
        m_c = compute_metrics(df, "deploy_composite_mean")

        records.append({
            "obs_noise_sd": float(noise_sd),
            "deployment_rate": m_g["deployment_rate"],
            "gate_unsafe_deploy": m_g["unsafe_deployment_rate"],
            "composite_unsafe_deploy": m_c["unsafe_deployment_rate"],
            "gate_unsafe_among_deployed": m_g["unsafe_among_deployed"],
            "composite_unsafe_among_deployed": m_c["unsafe_among_deployed"],
        })

    return pd.DataFrame(records)


# ── Epic Sepsis Model case scenario ─────────────────────────────────────────

def epic_case_row() -> Dict[str, object]:
    """Construct a single-row case calibrated to the Epic Sepsis Model."""
    row = {"tool_id": "EPIC_CASE", "risk_tier": "high", "unsafe_true": 1}
    obs = {
        "G1_Safety": 0.58,       # vendor claims vs external validation gap
        "G2_Equity": np.nan,     # limited published subgroup analysis
        "G3_Documentation": 0.38, # proprietary, no model card
        "G4_Accountability": 0.52, # variable withdrawal authority
        "G5_Monitoring": 0.30,   # no predefined monitoring thresholds
    }
    for g in GATES:
        row[f"{g}_latent"] = np.nan
        row[f"{g}_missing"] = int(np.isnan(obs[g]))
        row[f"{g}_obs"] = obs[g]
    return row


# ── Figure generation ────────────────────────────────────────────────────────

def _style_ax(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def fig1_unsafe_rates(metrics: Dict, out_dir: Path) -> None:
    """Bar chart: unsafe deployment rate by governance method."""
    methods = ["Gates", "Composite (matched)", "Composite (mean)",
               "Composite (zero)", "Permissive"]
    colours = [C_GATE, "#67001F", C_COMP_MEAN, C_COMP_ZERO, C_PERMISSIVE]
    rates = [metrics[m]["unsafe_deployment_rate"] for m in methods]
    deploy_rates = [metrics[m]["deployment_rate"] for m in methods]
    ci_data = metrics.get("_ci", {})

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bars = ax.bar(methods, rates, color=colours, edgecolor="white", linewidth=0.8)

    # CI whiskers
    for i, m in enumerate(methods):
        if m in ci_data and "unsafe_deployment_rate" in ci_data[m]:
            lo, hi = ci_data[m]["unsafe_deployment_rate"]
            ax.errorbar(i, rates[i], yerr=[[rates[i] - lo], [hi - rates[i]]],
                        fmt="none", color="black", capsize=4, linewidth=1.2)

    ax.set_ylabel("Unsafe deployment rate\n(proportion of all tools)", fontsize=11)
    ax.set_title("Figure 1. Unsafe Deployment Rate by Governance Method", fontsize=12, pad=12)
    _style_ax(ax)
    ax.set_ylim(bottom=0)

    # Value labels
    for bar, val, dr in zip(bars, rates, deploy_rates):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
                f"{val:.3f}\n(dep={dr:.0%})", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    fig.savefig(out_dir / "fig1_unsafe_deploy_rate.png", dpi=300, bbox_inches="tight")
    fig.savefig(out_dir / "fig1_unsafe_deploy_rate.pdf", bbox_inches="tight")
    plt.close(fig)


def fig2_tradeoff_curve(df: pd.DataFrame, out_dir: Path) -> None:
    """Deployment rate vs unsafe-among-deployed for composite scoring."""
    scores = df["composite_score_mean"].to_numpy()
    unsafe = df["unsafe_true"].to_numpy().astype(bool)

    thresholds = np.linspace(np.quantile(scores, 0.02), np.quantile(scores, 0.98), 40)
    deploy_rates, unsafe_rates, unsafe_among = [], [], []
    for t in thresholds:
        dep = scores >= t
        dr = float(dep.mean())
        ur = float((dep & unsafe).mean())
        ua = float(unsafe[dep].mean()) if dep.sum() > 0 else 0.0
        deploy_rates.append(dr)
        unsafe_rates.append(ur)
        unsafe_among.append(ua)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    ax1.plot(deploy_rates, unsafe_rates, "o-", color=C_COMP_MEAN, markersize=4)
    ax1.set_xlabel("Deployment rate", fontsize=11)
    ax1.set_ylabel("Unsafe deployment rate", fontsize=11)
    ax1.set_title("A. Composite threshold trade-off", fontsize=11)
    _style_ax(ax1)

    ax2.plot(deploy_rates, unsafe_among, "s-", color=C_COMP_MEAN, markersize=4)
    ax2.set_xlabel("Deployment rate", fontsize=11)
    ax2.set_ylabel("Proportion unsafe among deployed", fontsize=11)
    ax2.set_title("B. Contamination rate", fontsize=11)
    _style_ax(ax2)

    fig.suptitle("Figure 2. Composite-Score Threshold Trade-Off", fontsize=12, y=1.02)
    plt.tight_layout()
    fig.savefig(out_dir / "fig2_composite_tradeoff.png", dpi=300, bbox_inches="tight")
    fig.savefig(out_dir / "fig2_composite_tradeoff.pdf", bbox_inches="tight")
    plt.close(fig)


def fig3_gate_failures(df: pd.DataFrame, cfg: SimConfig, out_dir: Path) -> None:
    """Stacked bar: gate failure frequency by safety state."""
    tiers = df["risk_tier"].to_numpy()
    unsafe = df["unsafe_true"].to_numpy().astype(bool)
    safe = ~unsafe

    fail_safe = {g: 0 for g in GATES}
    fail_unsafe = {g: 0 for g in GATES}

    for i in range(len(df)):
        thr = cfg.thresholds_high if tiers[i] == "high" else cfg.thresholds_standard
        for g in GATES:
            obs = df.at[i, f"{g}_obs"]
            passed = (not pd.isna(obs)) and (float(obs) >= float(thr[g]))
            if not passed:
                if unsafe[i]:
                    fail_unsafe[g] += 1
                else:
                    fail_safe[g] += 1

    n_safe = int(safe.sum())
    n_unsafe = int(unsafe.sum())

    labels = [GATE_LABELS.get(g, g) for g in GATES]
    safe_rates = [fail_safe[g] / n_safe for g in GATES]
    unsafe_rates = [fail_unsafe[g] / n_unsafe for g in GATES]

    x = np.arange(len(GATES))
    w = 0.35

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.bar(x - w / 2, safe_rates, w, label="Safe tools", color=C_SAFE, edgecolor="white")
    ax.bar(x + w / 2, unsafe_rates, w, label="Unsafe tools", color=C_UNSAFE, edgecolor="white")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Failure frequency (proportion)", fontsize=11)
    ax.set_title("Figure 3. Gate Failure Frequency by Domain and Safety State", fontsize=12, pad=12)
    ax.legend(frameon=False)
    _style_ax(ax)
    plt.tight_layout()
    fig.savefig(out_dir / "fig3_gate_failures.png", dpi=300, bbox_inches="tight")
    fig.savefig(out_dir / "fig3_gate_failures.pdf", bbox_inches="tight")
    plt.close(fig)


def fig4_epic_case(case_df: pd.DataFrame, cfg: SimConfig, out_dir: Path) -> None:
    """Epic case: evidence profile and deployment decisions."""
    row = case_df.iloc[0]
    obs_vals = []
    thr_vals = []
    for g in GATES:
        o = row[f"{g}_obs"]
        obs_vals.append(o if not pd.isna(o) else 0.0)
        thr_vals.append(cfg.thresholds_high[g])

    labels = [GATE_LABELS.get(g, g) for g in GATES]
    x = np.arange(len(GATES))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={"width_ratios": [3, 2]})

    # Panel A: evidence profile
    bars = ax1.bar(x, obs_vals, color=[C_UNSAFE if obs_vals[i] < thr_vals[i] else C_SAFE
                                        for i in range(len(GATES))],
                   edgecolor="white")
    ax1.plot(x, thr_vals, "k--", label="High-risk threshold", linewidth=1.5)

    # Mark missing
    for i, g in enumerate(GATES):
        if pd.isna(row[f"{g}_obs"]):
            ax1.text(i, 0.02, "MISSING", ha="center", fontsize=8, color="white",
                     fontweight="bold", rotation=90)

    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=9)
    ax1.set_ylabel("Observed evidence score", fontsize=11)
    ax1.set_title("A. Evidence profile", fontsize=11)
    ax1.set_ylim(0, 1.0)
    ax1.legend(frameon=False, fontsize=9)
    _style_ax(ax1)

    # Panel B: deployment decisions
    methods = ["Non-compensatory\ngates", "Composite\n(mean impute)", "Composite\n(zero impute)"]
    cols = ["deploy_gate", "deploy_composite_mean", "deploy_composite_zero"]
    decisions = [int(row[c]) for c in cols]
    colours = [C_SAFE if d == 0 else C_UNSAFE for d in decisions]
    dec_labels = ["NO-GO" if d == 0 else "GO" for d in decisions]

    bars2 = ax2.barh(range(len(methods)), decisions, color=colours, edgecolor="white", height=0.5)
    ax2.set_yticks(range(len(methods)))
    ax2.set_yticklabels(methods, fontsize=10)
    ax2.set_xlim(-0.1, 1.3)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(["NO-GO", "GO"], fontsize=10)
    for i, lbl in enumerate(dec_labels):
        ax2.text(decisions[i] + 0.05, i, lbl, va="center", fontsize=10, fontweight="bold")
    ax2.set_title("B. Deployment decisions", fontsize=11)
    _style_ax(ax2)

    fig.suptitle("Figure 4. Epic Sepsis Model Case Scenario", fontsize=12, y=1.02)
    plt.tight_layout()
    fig.savefig(out_dir / "fig4_epic_case.png", dpi=300, bbox_inches="tight")
    fig.savefig(out_dir / "fig4_epic_case.pdf", bbox_inches="tight")
    plt.close(fig)


def fig5_sensitivity(sens_df: pd.DataFrame, out_dir: Path) -> None:
    """Sensitivity: unsafe deployment rate vs threshold multiplier."""
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(sens_df["threshold_multiplier"], sens_df["gate_unsafe_deploy"],
            "o-", color=C_GATE, label="Non-compensatory gates", markersize=5)
    ax.plot(sens_df["threshold_multiplier"], sens_df["composite_unsafe_deploy"],
            "s-", color=C_COMP_MEAN, label="Composite (mean)", markersize=5)
    ax.set_xlabel("Threshold multiplier (relative to default)", fontsize=11)
    ax.set_ylabel("Unsafe deployment rate", fontsize=11)
    ax.set_title("Figure 5. Sensitivity to Threshold Calibration", fontsize=12, pad=12)
    ax.legend(frameon=False)
    _style_ax(ax)
    plt.tight_layout()
    fig.savefig(out_dir / "fig5_sensitivity.png", dpi=300, bbox_inches="tight")
    fig.savefig(out_dir / "fig5_sensitivity.pdf", bbox_inches="tight")
    plt.close(fig)


def fig6_noise_robustness(noise_df: pd.DataFrame, out_dir: Path) -> None:
    """Noise robustness: unsafe rate vs measurement noise."""
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(noise_df["obs_noise_sd"], noise_df["gate_unsafe_deploy"],
            "o-", color=C_GATE, label="Non-compensatory gates", markersize=5)
    ax.plot(noise_df["obs_noise_sd"], noise_df["composite_unsafe_deploy"],
            "s-", color=C_COMP_MEAN, label="Composite (mean)", markersize=5)
    ax.set_xlabel("Observation noise (SD)", fontsize=11)
    ax.set_ylabel("Unsafe deployment rate", fontsize=11)
    ax.set_title("Figure 6. Decision Consistency Under Measurement Noise",
                 fontsize=12, pad=12)
    ax.legend(frameon=False)
    _style_ax(ax)
    plt.tight_layout()
    fig.savefig(out_dir / "fig6_noise_robustness.png", dpi=300, bbox_inches="tight")
    fig.savefig(out_dir / "fig6_noise_robustness.pdf", bbox_inches="tight")
    plt.close(fig)


# ── Main ─────────────────────────────────────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Non-compensatory governance gates simulation study"
    )
    parser.add_argument("--config", type=str, default=None,
                        help="Path to JSON config file")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--n-tools", type=int, default=None)
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--skip-sensitivity", action="store_true")
    parser.add_argument("--skip-bootstrap", action="store_true")
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    if args.seed is not None:
        cfg = SimConfig(**{**asdict(cfg), "seed": args.seed,
                           "override_disallowed_gates": cfg.override_disallowed_gates,
                           "unsafe_gate_profile": cfg.unsafe_gate_profile,
                           "p_missing_safe": cfg.p_missing_safe,
                           "p_missing_unsafe": cfg.p_missing_unsafe,
                           "composite_weights": cfg.composite_weights})
    if args.n_tools is not None:
        cfg = SimConfig(**{**asdict(cfg), "n_tools": args.n_tools,
                           "override_disallowed_gates": cfg.override_disallowed_gates,
                           "unsafe_gate_profile": cfg.unsafe_gate_profile,
                           "p_missing_safe": cfg.p_missing_safe,
                           "p_missing_unsafe": cfg.p_missing_unsafe,
                           "composite_weights": cfg.composite_weights})

    out_dir = Path(args.output_dir) if args.output_dir else Path(__file__).parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Simulating portfolio ...")
    df = simulate_portfolio(cfg)

    # ── Decision rules ───────────────────────────────────────────────────
    print("Applying decision rules ...")
    df = decide_noncomp_gates(df, cfg)

    weights = cfg.composite_weights
    gate_deploy_rate = float(df["deploy_gate"].mean())
    print(f"  Gate deployment rate: {gate_deploy_rate:.3f}")

    # Composite scoring with NATURAL thresholds (not rate-matched)
    # This is the key comparison: composite at a threshold that produces
    # a SIMILAR deployment rate to gates, showing that it lets through
    # unsafe tools while gates do not.

    # Composite (mean imputation) at threshold producing ~2x gate rate
    # (typical institutional choice — moderate restrictiveness)
    tmp = decide_weighted_composite(df, weights, threshold=0.0, missing_mode="mean")
    scores_mean = tmp["composite_score_mean"].to_numpy()

    # Find threshold that yields comparable deployment rate to gates
    thr_matched = set_threshold_to_match_rate(scores_mean, gate_deploy_rate)
    # Find threshold that yields a moderately permissive rate (~2x gates)
    thr_moderate = set_threshold_to_match_rate(scores_mean,
                                                min(gate_deploy_rate * 2.2, 0.85))

    df = decide_weighted_composite(df, weights, threshold=thr_matched,
                                   missing_mode="mean", col_suffix="matched")
    df = decide_weighted_composite(df, weights, threshold=thr_moderate,
                                   missing_mode="mean")

    # Composite (zero imputation) at moderate threshold
    tmp = decide_weighted_composite(df, weights, threshold=0.0, missing_mode="zero",
                                    col_suffix="zero_tmp")
    scores_zero = tmp["composite_score_zero_tmp"].to_numpy()
    thr_zero_mod = set_threshold_to_match_rate(scores_zero,
                                                min(gate_deploy_rate * 2.2, 0.85))
    df = decide_weighted_composite(df, weights, threshold=thr_zero_mod,
                                   missing_mode="zero")

    # Permissive baseline
    df = decide_permissive(df, cfg)

    # ── Metrics ──────────────────────────────────────────────────────────
    print("Computing metrics ...")
    method_cols = {
        "Gates": "deploy_gate",
        "Composite (matched)": "deploy_composite_matched",
        "Composite (mean)": "deploy_composite_mean",
        "Composite (zero)": "deploy_composite_zero",
        "Permissive": "deploy_permissive",
    }
    metrics = {}
    for label, col in method_cols.items():
        metrics[label] = compute_metrics(df, col)

    metrics["Gates"]["override_rate"] = float(df["override_used"].mean())
    metrics["Gates"]["n_overrides"] = int(df["override_used"].sum())

    # Bootstrap CIs
    ci_data = {}
    if not args.skip_bootstrap:
        print("Bootstrapping confidence intervals ...")
        for label, col in method_cols.items():
            ci_data[label] = {}
            for mk in ["unsafe_deployment_rate", "unsafe_among_deployed"]:
                ci_data[label][mk] = bootstrap_ci(df, col, mk, n_boot=cfg.n_bootstrap,
                                                   seed=cfg.seed + 42)
    metrics["_ci"] = ci_data

    # ── Save data ────────────────────────────────────────────────────────
    print("Saving outputs ...")
    df.to_csv(out_dir / "simulation_outputs.csv", index=False)

    summary = {
        "config": {
            "n_tools": cfg.n_tools,
            "seed": cfg.seed,
            "p_high_risk": cfg.p_high_risk,
            "p_unsafe_standard": cfg.p_unsafe_standard,
            "p_unsafe_high": cfg.p_unsafe_high,
            "obs_noise_sd": cfg.obs_noise_sd,
            "maturity_effect_sd": cfg.maturity_effect_sd,
            "override": {
                "allow_override": cfg.allow_override,
                "override_prob": cfg.override_prob,
                "override_max_failed_gates": cfg.override_max_failed_gates,
                "override_disallowed_gates": list(cfg.override_disallowed_gates),
            },
            "thresholds_standard": cfg.thresholds_standard,
            "thresholds_high": cfg.thresholds_high,
            "weights": weights,
            "composite_thresholds": {
                "matched_to_gates": thr_matched,
                "moderate_mean": thr_moderate,
                "moderate_zero": thr_zero_mod,
                "gate_deploy_rate": gate_deploy_rate,
            },
        },
        "metrics": {k: v for k, v in metrics.items() if k != "_ci"},
        "bootstrap_ci": {k: {mk: list(v) for mk, v in ci.items()}
                         for k, ci in ci_data.items()},
    }
    (out_dir / "metrics_summary.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )

    # ── Figures ──────────────────────────────────────────────────────────
    print("Generating figures ...")
    fig1_unsafe_rates(metrics, out_dir)
    fig2_tradeoff_curve(df, out_dir)
    fig3_gate_failures(df, cfg, out_dir)

    # ── Epic case ────────────────────────────────────────────────────────
    print("Running Epic case scenario ...")
    case = pd.DataFrame([epic_case_row()])
    case = decide_noncomp_gates(case, cfg)
    case = decide_weighted_composite(case, weights, threshold=thr_matched,
                                     missing_mode="mean", col_suffix="matched")
    case = decide_weighted_composite(case, weights, threshold=thr_moderate,
                                     missing_mode="mean")
    case = decide_weighted_composite(case, weights, threshold=thr_zero_mod,
                                     missing_mode="zero")
    case.to_csv(out_dir / "epic_case_outputs.csv", index=False)
    fig4_epic_case(case, cfg, out_dir)

    # ── Sensitivity analyses ─────────────────────────────────────────────
    if not args.skip_sensitivity:
        print("Running sensitivity analyses ...")
        sens_df = sensitivity_over_thresholds(
            df, cfg, weights,
            multipliers=np.linspace(0.6, 1.4, 17),
        )
        sens_df.to_csv(out_dir / "sensitivity_thresholds.csv", index=False)
        fig5_sensitivity(sens_df, out_dir)

        noise_df = noise_robustness(
            cfg, weights,
            noise_levels=np.linspace(0.01, 0.20, 15),
        )
        noise_df.to_csv(out_dir / "sensitivity_noise.csv", index=False)
        fig6_noise_robustness(noise_df, out_dir)

    # ── Summary to stdout ────────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("HEADLINE METRICS")
    print("=" * 72)
    header = f"{'Method':<22s} {'Deploy%':>8s} {'Unsafe%':>8s} {'SafeBlk%':>9s} {'Unsafe/Dep':>11s}"
    print(header)
    print("-" * len(header))
    for label in ["Gates", "Composite (matched)", "Composite (mean)",
                  "Composite (zero)", "Permissive"]:
        m = metrics[label]
        print(
            f"{label:<22s} {m['deployment_rate']:>8.3f} "
            f"{m['unsafe_deployment_rate']:>8.3f} "
            f"{m['safe_blocked_rate']:>9.3f} "
            f"{m['unsafe_among_deployed']:>11.3f}"
        )
    print(f"\nOverrides invoked: {metrics['Gates']['n_overrides']}")
    print(f"Outputs: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
