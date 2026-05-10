#!/usr/bin/env python3
"""
2-D Calibration Grid Sensitivity (I-08 Stage 5 execution)
Pipeline-owned execution. Produces 5 x 5 = 25 grid points over
portfolio-mix axis x unsafe-rate axis.
"""
from __future__ import annotations
import json
import sys
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import numpy as np
import pandas as pd

# import simulation engine
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from run_simulation import (
    SimConfig, simulate_portfolio,
    decide_noncomp_gates, decide_weighted_composite, decide_permissive,
    compute_metrics, bootstrap_ci, set_threshold_to_match_rate,
)

# ── Grid specification (Spec #1 of Stage 4) ────────────────────────────────
P_HIGH_RISK_LEVELS  = [0.10, 0.20, 0.30, 0.40, 0.50]
P_UNSAFE_HIGH_LEVELS = [0.20, 0.30, 0.35, 0.45, 0.55]
RATIO_STD_TO_HIGH = 0.15 / 0.35   # preserve high:standard relative magnitude

WEIGHTS = {
    "G1_Safety": 0.30, "G2_Equity": 0.15, "G3_Documentation": 0.15,
    "G4_Accountability": 0.15, "G5_Monitoring": 0.25,
}
COMPOSITE_MODERATE_MAX_DEPLOY_RATE = 0.85

DEFAULT_CFG = SimConfig()  # all other params at default

# ── Run grid ───────────────────────────────────────────────────────────────
records = []
total = len(P_HIGH_RISK_LEVELS) * len(P_UNSAFE_HIGH_LEVELS)
i = 0
for p_high in P_HIGH_RISK_LEVELS:
    for p_unsafe_high in P_UNSAFE_HIGH_LEVELS:
        i += 1
        p_unsafe_std = p_unsafe_high * RATIO_STD_TO_HIGH

        cfg_dict = asdict(DEFAULT_CFG)
        cfg_dict["p_high_risk"] = p_high
        cfg_dict["p_unsafe_high"] = p_unsafe_high
        cfg_dict["p_unsafe_standard"] = p_unsafe_std
        cfg_dict["override_disallowed_gates"] = tuple(cfg_dict["override_disallowed_gates"])
        cfg_dict["unsafe_gate_profile"] = {k: tuple(v) for k, v in cfg_dict["unsafe_gate_profile"].items()}
        cfg = SimConfig(**cfg_dict)

        df = simulate_portfolio(cfg)
        df = decide_noncomp_gates(df, cfg)

        gate_rate = float(df["deploy_gate"].mean())
        if not (0 < gate_rate < 1):
            continue

        # composite-matched threshold
        tmp = decide_weighted_composite(df, WEIGHTS, threshold=0.0, missing_mode="mean")
        thr_matched  = set_threshold_to_match_rate(tmp["composite_score_mean"].to_numpy(), gate_rate)
        # composite-moderate at 2.2x gate rate, capped to match the engine.
        target_mod = min(COMPOSITE_MODERATE_MAX_DEPLOY_RATE, gate_rate * 2.2)
        thr_moderate = set_threshold_to_match_rate(tmp["composite_score_mean"].to_numpy(), target_mod)

        df_m  = decide_weighted_composite(df, WEIGHTS, threshold=thr_matched,
                                          missing_mode="mean", col_suffix="mean_matched")
        df_md = decide_weighted_composite(df_m, WEIGHTS, threshold=thr_moderate,
                                          missing_mode="mean", col_suffix="mean_moderate")
        df_p  = decide_permissive(df_md, cfg)

        m_g = compute_metrics(df_p, "deploy_gate")
        m_cm = compute_metrics(df_p, "deploy_composite_mean_matched")
        m_cM = compute_metrics(df_p, "deploy_composite_mean_moderate")
        m_pe = compute_metrics(df_p, "deploy_permissive")

        # Bootstrap CI on gate and composite-moderate unsafe rates
        ci_g  = bootstrap_ci(df_p, "deploy_gate", "unsafe_deployment_rate",
                             n_boot=cfg.n_bootstrap, seed=cfg.seed)
        ci_cM = bootstrap_ci(df_p, "deploy_composite_mean_moderate", "unsafe_deployment_rate",
                             n_boot=cfg.n_bootstrap, seed=cfg.seed)

        records.append({
            "p_high_risk": p_high,
            "p_unsafe_high": p_unsafe_high,
            "p_unsafe_standard": round(p_unsafe_std, 4),
            "gate_deploy_rate": round(m_g["deployment_rate"], 4),
            "gate_unsafe_rate": round(m_g["unsafe_deployment_rate"], 4),
            "gate_unsafe_ci_lo": round(ci_g[0], 4),
            "gate_unsafe_ci_hi": round(ci_g[1], 4),
            "comp_mod_deploy_rate": round(m_cM["deployment_rate"], 4),
            "comp_mod_unsafe_rate": round(m_cM["unsafe_deployment_rate"], 4),
            "comp_mod_unsafe_ci_lo": round(ci_cM[0], 4),
            "comp_mod_unsafe_ci_hi": round(ci_cM[1], 4),
            "comp_matched_unsafe_rate": round(m_cm["unsafe_deployment_rate"], 4),
            "perm_unsafe_rate": round(m_pe["unsafe_deployment_rate"], 4),
            "thr_moderate": round(thr_moderate, 4),
        })
        print(f"[{i:>2}/{total}] p_hi={p_high:.2f} p_un={p_unsafe_high:.2f} | "
              f"gate={m_g['unsafe_deployment_rate']:.3f} "
              f"compMod={m_cM['unsafe_deployment_rate']:.3f}", flush=True)

# ── Save ───────────────────────────────────────────────────────────────────
out = pd.DataFrame(records)
out_dir = ROOT / "outputs" / "grid_2d"
out_dir.mkdir(parents=True, exist_ok=True)
out.to_csv(out_dir / "calibration_grid_2d.csv", index=False)

# Pivot tables for compact reporting
gate_pivot = out.pivot(index="p_high_risk", columns="p_unsafe_high",
                       values="gate_unsafe_rate")
comp_pivot = out.pivot(index="p_high_risk", columns="p_unsafe_high",
                       values="comp_mod_unsafe_rate")
gate_pivot.to_csv(out_dir / "table_G1_gate_unsafe_grid.csv")
comp_pivot.to_csv(out_dir / "table_G2_composite_unsafe_grid.csv")

# Summary statistics
summary = {
    "n_grid_points": len(out),
    "gate_unsafe_max":   float(out["gate_unsafe_rate"].max()),
    "gate_unsafe_mean":  float(out["gate_unsafe_rate"].mean()),
    "gate_unsafe_n_zero": int((out["gate_unsafe_rate"] == 0.0).sum()),
    "comp_mod_unsafe_max":  float(out["comp_mod_unsafe_rate"].max()),
    "comp_mod_unsafe_mean": float(out["comp_mod_unsafe_rate"].mean()),
    "gate_advantage_preserved_all_points": bool(
        (out["gate_unsafe_rate"] < out["comp_mod_unsafe_rate"]).all()
    ),
    "gate_advantage_preserved_or_equal":  bool(
        (out["gate_unsafe_rate"] <= out["comp_mod_unsafe_rate"]).all()
    ),
    "max_gate_minus_comp_diff": float(
        (out["gate_unsafe_rate"] - out["comp_mod_unsafe_rate"]).max()
    ),
}
with open(out_dir / "summary_stats.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== GATE UNSAFE-DEPLOYMENT RATE GRID (rows: p_high_risk, cols: p_unsafe_high) ===")
print(gate_pivot.round(4).to_string())
print("\n=== COMPOSITE-MODERATE UNSAFE-DEPLOYMENT RATE GRID ===")
print(comp_pivot.round(4).to_string())
print("\n=== SUMMARY ===")
for k, v in summary.items():
    print(f"  {k:<42} = {v}")
