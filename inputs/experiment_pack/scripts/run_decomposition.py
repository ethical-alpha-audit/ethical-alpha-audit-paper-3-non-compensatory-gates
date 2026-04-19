#!/usr/bin/env python3
"""A02: Gate Decomposition Comparison — Stage 3 (CORRECTED for NaN handling).

All decompositions evaluated WITHOUT overrides for consistent comparison.
NaN observations treated as gate failure (matching baseline engine logic).
"""
import json, os, sys, hashlib
import numpy as np, pandas as pd
from datetime import datetime, timezone

sys.path.insert(0, "/home/claude/evidence/gates_sim_hardened/gates_simulation_publication_hardened_v2")
from run_simulation import (SimConfig, load_config, simulate_portfolio, GATES,
                             decide_noncomp_gates, bootstrap_ci)

OUTPUT_DIR = "/home/claude/experiments/A02_decomposition_comparison"
PARAMS_PATH = "/home/claude/evidence/gates_sim_hardened/gates_simulation_publication_hardened_v2/params_default.json"
SEED = 20260304; N_TOOLS = 1000; D3_NOISE_SEED = 42
LOCKED_PARAMS_HASH = "ed8a57ecc3711607b335aa79abf0059e27dcb67716633fc0f2eb0913e774dd9d"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
    return h.hexdigest()

def gpass(obs, thr):
    return (~pd.isna(obs)) & (obs.values >= thr)

def matched_threshold_search(scores, target_rate):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        rate = (scores >= mid).mean()
        if abs(rate - target_rate) < 0.001: return mid, rate
        if rate > target_rate: lo = mid
        else: hi = mid
    return mid, (scores >= mid).mean()

def eval_decomp(did, gp_list, gs_list, unsafe, ng, perm_min, weights):
    n = len(unsafe)
    nc = np.ones(n, bool)
    for gp in gp_list: nc &= gp
    nc_rate = nc.mean(); nc_unsafe = (nc & unsafe).sum() / n
    nc_ci = tuple(bootstrap_ci(nc & unsafe, n_boot=1000, seed=99)) if nc_unsafe > 0 else (0.0, 0.0)

    sa = np.column_stack([np.where(np.isnan(s), 0.0, s) for s in gs_list])
    w = np.array(weights); scores = (sa * w).sum(axis=1)

    mt, mr = matched_threshold_search(scores, nc_rate)
    md = scores >= mt; mu = (md & unsafe).sum() / n

    fd = scores >= 0.50; fr = fd.mean(); fu = (fd & unsafe).sum() / n

    gc = np.zeros(n)
    for gp in gp_list: gc += gp.astype(float)
    pd_ = gc >= perm_min; pr = pd_.mean(); pu = (pd_ & unsafe).sum() / n

    return {"decomposition_id": did, "n_gates": ng,
        "noncomp": {"deployment_rate": round(float(nc_rate),4), "unsafe_deployment_rate": round(float(nc_unsafe),4),
                     "ci_lower": round(float(nc_ci[0]),4), "ci_upper": round(float(nc_ci[1]),4)},
        "comp_matched": {"threshold": round(float(mt),4), "deployment_rate": round(float(mr),4),
                          "unsafe_deployment_rate": round(float(mu),4)},
        "comp_fixed050": {"threshold": 0.50, "deployment_rate": round(float(fr),4),
                           "unsafe_deployment_rate": round(float(fu),4)},
        "permissive": {"min_gates": perm_min, "deployment_rate": round(float(pr),4),
                        "unsafe_deployment_rate": round(float(pu),4)}}

def main():
    start = datetime.now(timezone.utc).isoformat()
    assert sha256_file(PARAMS_PATH) == LOCKED_PARAMS_HASH, "HALT: params hash"

    cfg = load_config(PARAMS_PATH); np.random.seed(SEED)
    df = simulate_portfolio(cfg); assert len(df) == N_TOOLS
    unsafe = df["unsafe_true"].values.astype(bool)
    tiers = df["risk_tier"].values

    g1, g2, g3, g4, g5 = [df[f"{g}_obs"] for g in GATES]
    thr = {g: np.where(tiers=="high", cfg.thresholds_high[g], cfg.thresholds_standard[g]) for g in GATES}
    g1p, g2p, g3p, g4p, g5p = [gpass(df[f"{g}_obs"], thr[g]) for g in GATES]

    # D0 reference with overrides
    df_ref = decide_noncomp_gates(df.copy(), cfg)
    d0_ref_rate = df_ref["deploy_gate"].mean()

    R = {}
    R["D0"] = eval_decomp("D0", [g1p,g2p,g3p,g4p,g5p], [g1.values,g2.values,g3.values,g4.values,g5.values],
                           unsafe, 5, 3, [0.30,0.15,0.15,0.15,0.25])
    print(f"D0 no-override: deploy={R['D0']['noncomp']['deployment_rate']}, D0 with-override ref: {d0_ref_rate:.4f}")

    R["D1"] = eval_decomp("D1", [g1p&g5p, g2p&g4p, g3p],
        [np.nanmean(np.c_[g1.values,g5.values],1), np.nanmean(np.c_[g2.values,g4.values],1), g3.values],
        unsafe, 3, 2, [0.55,0.30,0.15])

    R["D2"] = eval_decomp("D2", [g1p, g2p, g3p&g4p, g5p],
        [g1.values, g2.values, np.nanmean(np.c_[g3.values,g4.values],1), g5.values],
        unsafe, 4, 3, [0.30,0.15,0.30,0.25])

    rng3 = np.random.RandomState(D3_NOISE_SEED)
    g1a = np.where(pd.isna(g1), np.nan, np.clip(g1.values+rng3.normal(0,.05,N_TOOLS),0,1))
    g1b = np.where(pd.isna(g1), np.nan, np.clip(g1.values+rng3.normal(0,.05,N_TOOLS),0,1))
    thr_sp = np.where(tiers=="high", 0.60, 0.50)
    R["D3"] = eval_decomp("D3", [gpass(pd.Series(g1a),thr["G1_Safety"]), gpass(pd.Series(g1b),thr_sp),
                                   g2p, g3p, g4p, g5p],
        [g1a, g1b, g2.values, g3.values, g4.values, g5.values],
        unsafe, 6, 4, [0.15,0.15,0.15,0.15,0.15,0.25])

    end = datetime.now(timezone.utc).isoformat()

    out = {"experiment_id":"A02","seed":SEED,"n_tools":N_TOOLS,"d3_noise_seed":D3_NOISE_SEED,
           "params_hash":sha256_file(PARAMS_PATH),"start_time":start,"end_time":end,
           "d4_excluded":True,"d4_exclusion_reason":"Simulation lacks required observable features",
           "note":f"All decompositions without overrides. D0 with-overrides={d0_ref_rate:.4f}",
           "decompositions":R}
    with open(os.path.join(OUTPUT_DIR,"decomposition_results.json"),"w") as f: json.dump(out,f,indent=2)

    with open(os.path.join(OUTPUT_DIR,"decomposition_summary.csv"),"w") as f:
        f.write("decomposition_id,n_gates,decision_rule,threshold_value,deployment_rate,unsafe_deployment_rate,unsafe_ci_lower,unsafe_ci_upper\n")
        for did in ["D0","D1","D2","D3"]:
            r=R[did]; nc=r["noncomp"]; cm=r["comp_matched"]; cf=r["comp_fixed050"]; pm=r["permissive"]
            f.write(f"{did},{r['n_gates']},noncomp,per_gate,{nc['deployment_rate']},{nc['unsafe_deployment_rate']},{nc['ci_lower']},{nc['ci_upper']}\n")
            f.write(f"{did},{r['n_gates']},comp_matched,{cm['threshold']},{cm['deployment_rate']},{cm['unsafe_deployment_rate']},,\n")
            f.write(f"{did},{r['n_gates']},comp_fixed050,{cf['threshold']},{cf['deployment_rate']},{cf['unsafe_deployment_rate']},,\n")
            f.write(f"{did},{r['n_gates']},permissive,{pm['min_gates']},{pm['deployment_rate']},{pm['unsafe_deployment_rate']},,\n")

    print(f"\n=== A02 COMPLETE === Portfolio: n={N_TOOLS}, unsafe={unsafe.sum()}")
    for did in ["D0","D1","D2","D3"]:
        r=R[did]
        print(f"{did}({r['n_gates']}g): NC deploy={r['noncomp']['deployment_rate']:.3f} unsafe={r['noncomp']['unsafe_deployment_rate']:.4f} | "
              f"Comp050 deploy={r['comp_fixed050']['deployment_rate']:.3f} unsafe={r['comp_fixed050']['unsafe_deployment_rate']:.4f} | "
              f"Perm deploy={r['permissive']['deployment_rate']:.3f} unsafe={r['permissive']['unsafe_deployment_rate']:.4f}")

    print(f"\n=== SAFETY ADVANTAGE ===")
    for did in ["D0","D1","D2","D3"]:
        nu=R[did]["noncomp"]["unsafe_deployment_rate"]; cu=R[did]["comp_fixed050"]["unsafe_deployment_rate"]
        s = "ADVANTAGE" if nu<cu else ("BOTH ZERO" if nu==0 and cu==0 else "EQUIV" if nu==cu else "COMP BETTER")
        print(f"  {did}: NC={nu:.4f} Comp050={cu:.4f} → {s}")

if __name__=="__main__": main()
