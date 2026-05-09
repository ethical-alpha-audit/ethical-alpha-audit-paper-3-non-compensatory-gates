#!/usr/bin/env python3
"""Bootstrap CI for CH-2 crossover r* via resampling the underlying primary-model portfolio."""
import sys, json, numpy as np, pandas as pd
from dataclasses import asdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from run_simulation import (SimConfig, simulate_portfolio, decide_noncomp_gates,
    decide_weighted_composite, decide_permissive, set_threshold_to_match_rate)

WEIGHTS = {"G1_Safety": 0.30, "G2_Equity": 0.15, "G3_Documentation": 0.15,
           "G4_Accountability": 0.15, "G5_Monitoring": 0.25}

def build_cfg():
    d = asdict(SimConfig())
    d["override_disallowed_gates"] = tuple(d["override_disallowed_gates"])
    d["unsafe_gate_profile"] = {k: tuple(v) for k, v in d["unsafe_gate_profile"].items()}
    return SimConfig(**d)

cfg = build_cfg()
df = simulate_portfolio(cfg)
df = decide_noncomp_gates(df, cfg)
gate_rate = float(df["deploy_gate"].mean())
tmp = decide_weighted_composite(df, WEIGHTS, threshold=0.0, missing_mode="mean")
thr_mod = set_threshold_to_match_rate(tmp["composite_score_mean"].to_numpy(), min(0.85, gate_rate*2.2))
df = decide_weighted_composite(df, WEIGHTS, threshold=thr_mod, missing_mode="mean", col_suffix="mean_moderate")

ratios = np.array([0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0])

def loss(deploy, unsafe, c_fp, c_fn):
    fp = (deploy & unsafe).sum() / len(deploy)
    fn = ((~deploy) & (~unsafe)).sum() / len(deploy)
    return c_fp*fp + c_fn*fn

def crossover(deploy_g, deploy_cM, unsafe):
    diffs = []
    for r in ratios:
        Lg = loss(deploy_g, unsafe, 1.0, r)
        Lc = loss(deploy_cM, unsafe, 1.0, r)
        diffs.append(Lg - Lc)
    diffs = np.array(diffs)
    for i in range(len(ratios)-1):
        if diffs[i] < 0 and diffs[i+1] > 0:
            x0, x1 = np.log10(ratios[i]), np.log10(ratios[i+1])
            y0, y1 = diffs[i], diffs[i+1]
            return float(10 ** (x0 - y0*(x1-x0)/(y1-y0)))
    return None

deploy_g  = df["deploy_gate"].to_numpy().astype(bool)
deploy_cM = df["deploy_composite_mean_moderate"].to_numpy().astype(bool)
unsafe    = df["unsafe_true"].to_numpy().astype(bool)

r_point = crossover(deploy_g, deploy_cM, unsafe)
print(f"point r* = {r_point:.4f}")

rng = np.random.default_rng(20260304)
n = len(df)
B = 1000
r_boot = []
for b in range(B):
    idx = rng.integers(0, n, n)
    r_b = crossover(deploy_g[idx], deploy_cM[idx], unsafe[idx])
    if r_b is not None:
        r_boot.append(r_b)
r_boot = np.array(r_boot)
lo, hi = np.percentile(r_boot, [2.5, 97.5])
print(f"r* point = {r_point:.4f}; bootstrap 95% CI ({len(r_boot)}/{B} converged): [{lo:.4f}, {hi:.4f}]")
print(f"median = {np.median(r_boot):.4f}")

with open(ROOT/"outputs"/"counter_hypothesis"/"ch2_crossover_ci.json", "w") as f:
    json.dump({
        "r_star_point": round(r_point, 4),
        "ci_low":  round(float(lo), 4),
        "ci_high": round(float(hi), 4),
        "n_bootstrap_converged": int(len(r_boot)),
        "n_bootstrap_total": B,
    }, f, indent=2)
