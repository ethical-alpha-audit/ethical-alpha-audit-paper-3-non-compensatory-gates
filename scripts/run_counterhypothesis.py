#!/usr/bin/env python3
"""
Counter-Hypothesis Simulations (I-09 Stage 5 execution)
Pipeline-owned execution.

CH-1: High-noise + low-latent-danger
CH-2: Cost-asymmetric loss analysis (post-hoc on primary heterogeneous model)
CH-3: Near-uniform high-quality evidence
"""
from __future__ import annotations
import json
import sys
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from run_simulation import (
    SimConfig, simulate_portfolio,
    decide_noncomp_gates, decide_weighted_composite, decide_permissive,
    compute_metrics, bootstrap_ci, set_threshold_to_match_rate,
    GATES, clip01,
)

WEIGHTS = {
    "G1_Safety": 0.30, "G2_Equity": 0.15, "G3_Documentation": 0.15,
    "G4_Accountability": 0.15, "G5_Monitoring": 0.25,
}
OUT = ROOT / "outputs" / "counter_hypothesis"
OUT.mkdir(parents=True, exist_ok=True)


def build_cfg(**overrides) -> SimConfig:
    d = asdict(SimConfig())
    d["override_disallowed_gates"] = tuple(d["override_disallowed_gates"])
    d["unsafe_gate_profile"] = {k: tuple(v) for k, v in d["unsafe_gate_profile"].items()}
    d.update(overrides)
    return SimConfig(**d)


def fn_fp_rates(df: pd.DataFrame, deploy_col: str) -> dict:
    """Compute false-negative and false-positive rates under symmetric definitions."""
    deploy = df[deploy_col].astype(bool).to_numpy()
    unsafe = df["unsafe_true"].astype(bool).to_numpy()
    safe   = ~unsafe
    # FP: deploying an unsafe tool (rate over total population)
    fp_rate = float((deploy & unsafe).sum() / len(df))
    # FN: blocking a safe tool (rate over total population)
    fn_rate = float((~deploy & safe).sum() / len(df))
    # rates among class
    fp_among_unsafe = float((deploy & unsafe).sum() / max(unsafe.sum(), 1))
    fn_among_safe   = float((~deploy & safe).sum() / max(safe.sum(), 1))
    return {
        "fp_rate_pop": fp_rate, "fn_rate_pop": fn_rate,
        "fp_among_unsafe": fp_among_unsafe, "fn_among_safe": fn_among_safe,
        "deployment_rate": float(deploy.mean()),
    }


def expected_loss(df: pd.DataFrame, deploy_col: str, c_fp: float, c_fn: float) -> float:
    """Expected loss = c_fp * P(deploy & unsafe) + c_fn * P(~deploy & safe), per tool."""
    r = fn_fp_rates(df, deploy_col)
    return c_fp * r["fp_rate_pop"] + c_fn * r["fn_rate_pop"]


def evaluate_three_rules(df: pd.DataFrame, cfg: SimConfig) -> tuple:
    """Return df after evaluating all three rules + threshold metadata."""
    df = decide_noncomp_gates(df, cfg)
    gate_rate = float(df["deploy_gate"].mean())
    if not (0 < gate_rate < 1):
        return None, None, None
    tmp = decide_weighted_composite(df, WEIGHTS, threshold=0.0, missing_mode="mean")
    thr_matched  = set_threshold_to_match_rate(tmp["composite_score_mean"].to_numpy(), gate_rate)
    target_mod   = min(gate_rate * 2.2, 0.85)
    thr_moderate = set_threshold_to_match_rate(tmp["composite_score_mean"].to_numpy(), target_mod)
    df = decide_weighted_composite(df, WEIGHTS, threshold=thr_matched,
                                   missing_mode="mean", col_suffix="mean_matched")
    df = decide_weighted_composite(df, WEIGHTS, threshold=thr_moderate,
                                   missing_mode="mean", col_suffix="mean_moderate")
    df = decide_permissive(df, cfg)
    return df, thr_matched, thr_moderate


# ──────────────────────────────────────────────────────────────────────────
# CH-1: High-noise + low-latent-danger
# ──────────────────────────────────────────────────────────────────────────
print("\n=== CH-1: High-noise + low-latent-danger ===")
cfg_ch1 = build_cfg(
    obs_noise_sd=0.20,         # high noise
    p_unsafe_high=0.05,        # low latent danger
    p_unsafe_standard=0.02,
)
df = simulate_portfolio(cfg_ch1)
df, thr_m, thr_M = evaluate_three_rules(df, cfg_ch1)
ch1_results = {}
for name, col in [("Gates", "deploy_gate"),
                  ("Composite (matched)",  "deploy_composite_mean_matched"),
                  ("Composite (moderate)", "deploy_composite_mean_moderate"),
                  ("Permissive",           "deploy_permissive")]:
    r = fn_fp_rates(df, col)
    m = compute_metrics(df, col)
    ci = bootstrap_ci(df, col, "unsafe_deployment_rate",
                      n_boot=cfg_ch1.n_bootstrap, seed=cfg_ch1.seed)
    ch1_results[name] = {
        "deployment_rate": round(r["deployment_rate"], 4),
        "unsafe_deployment_rate": round(m["unsafe_deployment_rate"], 4),
        "unsafe_ci_lo": round(ci[0], 4),
        "unsafe_ci_hi": round(ci[1], 4),
        "fn_rate_pop": round(r["fn_rate_pop"], 4),
        "fn_among_safe": round(r["fn_among_safe"], 4),
        "fp_among_unsafe": round(r["fp_among_unsafe"], 4),
        "loss_symmetric_c1": round(expected_loss(df, col, 1.0, 1.0), 4),
    }
    print(f"  {name:<22} | deploy={r['deployment_rate']:.3f} unsafe={m['unsafe_deployment_rate']:.4f} "
          f"FN(safe)={r['fn_among_safe']:.3f} FP(unsafe)={r['fp_among_unsafe']:.3f}")

# CH-1 interpretation
g_fn = ch1_results["Gates"]["fn_among_safe"]
c_fn = ch1_results["Composite (moderate)"]["fn_among_safe"]
fn_gap = g_fn - c_fn
ch1_interp = ("STRENGTHENS gate position" if fn_gap < 0.05
              else ("WEAKENS gate position" if fn_gap > 0.10
                    else "AMBIGUOUS — small gap"))
print(f"\n  CH-1 FN-rate gap (gates - composite-moderate) = {fn_gap:+.3f} -> {ch1_interp}")

with open(OUT / "ch1_high_noise_low_danger.json", "w") as f:
    json.dump({"results": ch1_results, "fn_rate_gap": fn_gap, "interpretation": ch1_interp}, f, indent=2)


# ──────────────────────────────────────────────────────────────────────────
# CH-2: Cost-asymmetric loss analysis (post-hoc on primary heterogeneous model)
# ──────────────────────────────────────────────────────────────────────────
print("\n=== CH-2: Cost-asymmetric loss analysis (primary heterogeneous model) ===")
cfg_primary = build_cfg()
dfp = simulate_portfolio(cfg_primary)
dfp, thr_m, thr_M = evaluate_three_rules(dfp, cfg_primary)

ratios = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0]
ch2_records = []
for r in ratios:
    # Fix c_fp = 1.0 ; c_fn = r ; expected loss per tool
    L_g  = expected_loss(dfp, "deploy_gate",                       c_fp=1.0, c_fn=r)
    L_cm = expected_loss(dfp, "deploy_composite_mean_matched",     c_fp=1.0, c_fn=r)
    L_cM = expected_loss(dfp, "deploy_composite_mean_moderate",    c_fp=1.0, c_fn=r)
    L_pe = expected_loss(dfp, "deploy_permissive",                  c_fp=1.0, c_fn=r)
    ch2_records.append({
        "cost_ratio_r": r,
        "loss_gates":           round(L_g, 5),
        "loss_comp_matched":    round(L_cm, 5),
        "loss_comp_moderate":   round(L_cM, 5),
        "loss_permissive":      round(L_pe, 5),
        "winner_g_vs_cM":       "Gates" if L_g < L_cM else ("Composite-mod" if L_cM < L_g else "Tie"),
    })
    print(f"  r={r:>6.2f} | gates={L_g:.4f}  comp-mod={L_cM:.4f}  perm={L_pe:.4f}  "
          f"-> {'Gates' if L_g < L_cM else 'Composite-mod':<14}")

ch2_df = pd.DataFrame(ch2_records)
ch2_df.to_csv(OUT / "ch2_cost_asymmetric_loss.csv", index=False)

# Find crossover ratio r* where gates and composite-moderate have equal loss
# (linear interpolation between bracketing ratios in log-space)
g = ch2_df["loss_gates"].to_numpy()
cM = ch2_df["loss_comp_moderate"].to_numpy()
diff = g - cM   # positive when gates worse
crossover = None
for i in range(len(ratios) - 1):
    if (diff[i] < 0) and (diff[i+1] > 0):
        # crossover between ratios[i] and ratios[i+1]; log-linear interpolation
        x0, x1 = np.log10(ratios[i]), np.log10(ratios[i+1])
        y0, y1 = diff[i], diff[i+1]
        x_cross = x0 - y0 * (x1 - x0) / (y1 - y0)
        crossover = float(10 ** x_cross)
        break

if crossover is None:
    if (diff <= 0).all():
        ch2_interp = ("STRENGTHENS — gates dominate composite-moderate at every cost ratio "
                      f"in [{ratios[0]}, {ratios[-1]}]; no crossover within tested range.")
    elif (diff >= 0).all():
        ch2_interp = ("CONTRADICTS — gates underperform composite-moderate at every tested "
                      "cost ratio; gate architecture is loss-suboptimal.")
    else:
        ch2_interp = "AMBIGUOUS — multiple crossings; manual inspection needed."
else:
    if crossover >= 1.0:
        ch2_interp = (f"STRENGTHENS with finite crossover — gates win when c_FN/c_FP <= {crossover:.2f}; "
                      f"composite-moderate wins above. Crossover above unit cost (gates win at symmetric).")
    else:
        ch2_interp = (f"PARTIALLY WEAKENS — crossover at r* = {crossover:.3f} < 1; "
                      f"composite-moderate wins under symmetric or moderately FN-asymmetric costs.")

print(f"\n  CH-2 crossover r* = {crossover}")
print(f"  CH-2 interpretation: {ch2_interp}")

with open(OUT / "ch2_summary.json", "w") as f:
    json.dump({"crossover_r_star": crossover, "interpretation": ch2_interp,
               "ratios_tested": ratios}, f, indent=2)


# ──────────────────────────────────────────────────────────────────────────
# CH-3: Near-uniform high-quality evidence
# Implementation: override gate-profile shifts so unsafe tools also draw from
# Beta(6, 2.5) (mean ≈ 0.71) and safe tools from Beta(8, 2) (mean ≈ 0.80).
# ──────────────────────────────────────────────────────────────────────────
print("\n=== CH-3: Near-uniform high-quality evidence ===")

# Custom simulator: zero out unsafe_gate_profile shifts and set high-quality params
cfg_ch3 = build_cfg(
    safe_beta_a=8.0, safe_beta_b=2.0,           # mean ≈ 0.80
    unsafe_beta_a=6.0, unsafe_beta_b=2.5,       # mean ≈ 0.71 (only 0.10 below safe)
    unsafe_gate_profile={g: (0.0, 0.0) for g in GATES},  # NO heterogeneity shifts
)
df3 = simulate_portfolio(cfg_ch3)
df3, _, _ = evaluate_three_rules(df3, cfg_ch3)
ch3_results = {}
for name, col in [("Gates", "deploy_gate"),
                  ("Composite (matched)",  "deploy_composite_mean_matched"),
                  ("Composite (moderate)", "deploy_composite_mean_moderate"),
                  ("Permissive",           "deploy_permissive")]:
    r = fn_fp_rates(df3, col)
    m = compute_metrics(df3, col)
    ci = bootstrap_ci(df3, col, "unsafe_deployment_rate",
                      n_boot=cfg_ch3.n_bootstrap, seed=cfg_ch3.seed)
    ch3_results[name] = {
        "deployment_rate": round(r["deployment_rate"], 4),
        "unsafe_deployment_rate": round(m["unsafe_deployment_rate"], 4),
        "unsafe_ci_lo": round(ci[0], 4),
        "unsafe_ci_hi": round(ci[1], 4),
        "fn_rate_pop": round(r["fn_rate_pop"], 4),
        "fn_among_safe": round(r["fn_among_safe"], 4),
        "fp_among_unsafe": round(r["fp_among_unsafe"], 4),
    }
    print(f"  {name:<22} | deploy={r['deployment_rate']:.3f} unsafe={m['unsafe_deployment_rate']:.4f} "
          f"FN(safe)={r['fn_among_safe']:.3f}")

g_us = ch3_results["Gates"]["unsafe_deployment_rate"]
cM_us = ch3_results["Composite (moderate)"]["unsafe_deployment_rate"]
ch3_interp = ("CONFIRMS uniform-quality convergence" if abs(g_us - cM_us) < 0.005
              else ("Gates RETAIN advantage" if g_us < cM_us
                    else "Gates UNDERPERFORM composite"))
print(f"\n  CH-3 gate-vs-composite-moderate unsafe gap = {(g_us - cM_us):+.4f} -> {ch3_interp}")

with open(OUT / "ch3_uniform_high_quality.json", "w") as f:
    json.dump({"results": ch3_results, "interpretation": ch3_interp}, f, indent=2)

# Composite summary
summary = {
    "CH-1": {"interpretation": ch1_interp,
             "fn_rate_gap_gates_minus_comp_mod": round(fn_gap, 4)},
    "CH-2": {"interpretation": ch2_interp,
             "crossover_r_star": crossover},
    "CH-3": {"interpretation": ch3_interp,
             "gate_unsafe_minus_comp_mod_unsafe": round(g_us - cM_us, 4)},
}
with open(OUT / "counter_hypothesis_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== COUNTER-HYPOTHESIS SUMMARY ===")
print(json.dumps(summary, indent=2))
