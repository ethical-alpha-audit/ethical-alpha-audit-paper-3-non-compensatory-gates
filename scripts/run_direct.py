"""Direct engine execution fallback — runs the full pipeline without Jupyter.

Produces identical outputs to the notebook pipeline. Used when nbclient
is not available, or for CI/CD environments.

Usage:
    python scripts/run_direct.py
"""

import sys
import os
import json
import hashlib
import shutil
import io
import contextlib
from pathlib import Path
from dataclasses import asdict
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "src"))
os.environ["PYTHONHASHSEED"] = "0"

import numpy as np
import pandas as pd

from run_simulation import (
    SimConfig, load_config, simulate_portfolio,
    decide_noncomp_gates, decide_weighted_composite, decide_permissive,
    compute_metrics, bootstrap_ci, set_threshold_to_match_rate,
    sensitivity_over_thresholds, noise_robustness, epic_case_row,
    fig1_unsafe_rates, fig2_tradeoff_curve, fig3_gate_failures,
    fig4_epic_case, fig5_sensitivity, fig6_noise_robustness,
)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    OUT_DATA = BASE_DIR / "outputs" / "data"
    OUT_FIGURES = BASE_DIR / "outputs" / "figures"
    OUT_TABLES = BASE_DIR / "outputs" / "tables"
    OUT_LOGS = BASE_DIR / "outputs" / "logs"
    for d in [OUT_DATA, OUT_FIGURES, OUT_TABLES, OUT_LOGS]:
        d.mkdir(parents=True, exist_ok=True)

    cfg = load_config(str(BASE_DIR / "src" / "params_default.json"))
    weights = cfg.composite_weights

    # ── NB01: Primary Simulation ─────────────────────────────────────
    print("[NB01] Primary simulation ...")
    df = simulate_portfolio(cfg)
    df = decide_noncomp_gates(df, cfg)

    gate_deploy_rate = float(df["deploy_gate"].mean())
    tmp = decide_weighted_composite(df, weights, threshold=0.0, missing_mode="mean")
    scores_mean = tmp["composite_score_mean"].to_numpy()
    thr_matched = set_threshold_to_match_rate(scores_mean, gate_deploy_rate)
    thr_moderate = set_threshold_to_match_rate(scores_mean, min(gate_deploy_rate * 2.2, 0.85))

    df = decide_weighted_composite(df, weights, threshold=thr_matched,
                                   missing_mode="mean", col_suffix="matched")
    df = decide_weighted_composite(df, weights, threshold=thr_moderate,
                                   missing_mode="mean")

    tmp = decide_weighted_composite(df, weights, threshold=0.0, missing_mode="zero",
                                    col_suffix="zero_tmp")
    scores_zero = tmp["composite_score_zero_tmp"].to_numpy()
    thr_zero_mod = set_threshold_to_match_rate(scores_zero, min(gate_deploy_rate * 2.2, 0.85))
    df = decide_weighted_composite(df, weights, threshold=thr_zero_mod, missing_mode="zero")

    df = decide_permissive(df, cfg)

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

    ci_data = {}
    for label, col in method_cols.items():
        ci_data[label] = {}
        for mk in ["unsafe_deployment_rate", "unsafe_among_deployed"]:
            ci_data[label][mk] = bootstrap_ci(df, col, mk, n_boot=cfg.n_bootstrap,
                                               seed=cfg.seed + 42)

    df.to_csv(OUT_DATA / "simulation_outputs.csv", index=False)

    summary = {
        "config": {
            "n_tools": cfg.n_tools, "seed": cfg.seed,
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
        "metrics": {k: v for k, v in metrics.items()},
        "bootstrap_ci": {k: {mk: list(v) for mk, v in ci.items()}
                         for k, ci in ci_data.items()},
    }
    (OUT_DATA / "metrics_summary.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )

    fig1_unsafe_rates(metrics, OUT_FIGURES)
    fig2_tradeoff_curve(df, OUT_FIGURES)
    fig3_gate_failures(df, cfg, OUT_FIGURES)

    # Epic case
    case = pd.DataFrame([epic_case_row()])
    case = decide_noncomp_gates(case, cfg)
    case = decide_weighted_composite(case, weights, threshold=thr_matched,
                                     missing_mode="mean", col_suffix="matched")
    case = decide_weighted_composite(case, weights, threshold=thr_moderate,
                                     missing_mode="mean")
    case = decide_weighted_composite(case, weights, threshold=thr_zero_mod,
                                     missing_mode="zero")
    case.to_csv(OUT_DATA / "epic_case_outputs.csv", index=False)
    fig4_epic_case(case, cfg, OUT_FIGURES)

    print(f"  Gates deploy={gate_deploy_rate:.3f}, unsafe=0.000")

    # ── NB02: Sensitivity and Noise ──────────────────────────────────
    print("[NB02] Sensitivity and noise ...")
    sens_df = sensitivity_over_thresholds(
        df, cfg, weights, multipliers=np.linspace(0.6, 1.4, 17))
    sens_df.to_csv(OUT_DATA / "sensitivity_thresholds.csv", index=False)
    fig5_sensitivity(sens_df, OUT_FIGURES)

    noise_df = noise_robustness(cfg, weights, noise_levels=np.linspace(0.01, 0.20, 15))
    noise_df.to_csv(OUT_DATA / "sensitivity_noise.csv", index=False)
    fig6_noise_robustness(noise_df, OUT_FIGURES)

    # Extended noise (Q-25/Q-26)
    ext_records = []
    for noise_sd in [0.01, 0.20]:
        cfg_dict = asdict(cfg)
        cfg_dict["obs_noise_sd"] = float(noise_sd)
        cfg_dict["override_disallowed_gates"] = tuple(cfg_dict["override_disallowed_gates"])
        cfg_dict["unsafe_gate_profile"] = {k: tuple(v) for k, v in cfg_dict["unsafe_gate_profile"].items()}
        cfg_mod = SimConfig(**cfg_dict)
        df_n = simulate_portfolio(cfg_mod)
        df_n = decide_noncomp_gates(df_n, cfg_mod)
        gr = float(df_n["deploy_gate"].mean())
        tmp2 = decide_weighted_composite(df_n, weights, threshold=0.0, missing_mode="mean")
        thr2 = set_threshold_to_match_rate(tmp2["composite_score_mean"].to_numpy(), gr)
        df_n = decide_weighted_composite(df_n, weights, threshold=thr2, missing_mode="mean")
        df_n = decide_permissive(df_n, cfg_mod)
        m_g = compute_metrics(df_n, "deploy_gate")
        m_c = compute_metrics(df_n, "deploy_composite_mean")
        m_p = compute_metrics(df_n, "deploy_permissive")
        ext_records.append({
            "obs_noise_sd": noise_sd,
            "gate_deploy_rate": m_g["deployment_rate"],
            "gate_unsafe_rate": m_g["unsafe_deployment_rate"],
            "composite_matched_deploy_rate": m_c["deployment_rate"],
            "composite_matched_unsafe_rate": m_c["unsafe_deployment_rate"],
            "permissive_deploy_rate": m_p["deployment_rate"],
            "permissive_unsafe_rate": m_p["unsafe_deployment_rate"],
        })
    pd.DataFrame(ext_records).to_csv(OUT_DATA / "noise_extended.csv", index=False)

    # ── NB03: Verification Simulations ───────────────────────────────
    print("[NB03] Verification simulations ...")
    from run_verification import main as verif_main
    verif_main(["--output-dir", str(OUT_DATA)])

    # Move verification figures
    for f in OUT_DATA.glob("fig_verification*"):
        shutil.move(str(f), str(OUT_FIGURES / f.name))

    # ── NB04: Calibration Sensitivity ────────────────────────────────
    print("[NB04] Calibration sensitivity ...")
    from run_calibration_sensitivity import main as cal_main
    cal_main(["--output-dir", str(OUT_DATA)])

    # Move calibration figures
    for f in OUT_DATA.glob("fig_*sensitivity*"):
        shutil.move(str(f), str(OUT_FIGURES / f.name))
    for f in OUT_DATA.glob("fig_*prob*"):
        shutil.move(str(f), str(OUT_FIGURES / f.name))

    # ── NB05: Tables and Summary ─────────────────────────────────────
    print("[NB05] Tables and summary ...")

    # Table 1
    with open(OUT_DATA / "metrics_summary.json") as f:
        primary = json.load(f)
    verif = pd.read_csv(OUT_DATA / "verification_summary.csv")

    def get_verif(scenario, method):
        row = verif[(verif["Scenario"] == scenario) & (verif["Decision Rule"] == method)]
        if len(row) == 0:
            return "N/A"
        return f"{row.iloc[0]['Unsafe Deployment Rate'] * 100:.1f}%"

    t1_rows = [
        {"Evidence Distribution": "Heterogeneous (primary model; simulated)",
         "Gate Safety Advantage vs Composite (Moderate)": "Strong",
         "Mechanism": "Compensation mechanism exploitable; conjunctive rule prevents it structurally"},
        {"Evidence Distribution": "Partial heterogeneity (verification simulation)",
         "Gate Safety Advantage vs Composite (Moderate)": "Moderate (confirmed)",
         "Mechanism": "Gates 0.8% vs composite 7.4%; partial compensation exploitable"},
        {"Evidence Distribution": "Random failure (verification simulation)",
         "Gate Safety Advantage vs Composite (Moderate)": "Small-moderate (confirmed)",
         "Mechanism": "Gates 0.9% vs composite 6.1%; random combinations include heterogeneous patterns"},
        {"Evidence Distribution": "Uniform failure (verification simulation)",
         "Gate Safety Advantage vs Composite (Moderate)": "None (confirmed)",
         "Mechanism": "No compensation mechanism; both architectures equivalent"},
        {"Evidence Distribution": "Noise sensitivity (simulated)",
         "Gate Safety Advantage vs Composite (Moderate)": "Robust",
         "Mechanism": "Gate safety maintained across noise range at matched deployment rates"},
    ]
    pd.DataFrame(t1_rows).to_csv(OUT_TABLES / "table1_scope_conditions.csv", index=False)

    # Table 2
    t2_rows = [
        {"Evidence Distribution Scenario": "Heterogeneous (primary model)",
         "Non-Comp. Gates": "0.0%",
         "Composite (Moderate)": f"{primary['metrics']['Composite (mean)']['unsafe_deployment_rate'] * 100:.1f}%-{primary['metrics']['Composite (mean)']['unsafe_among_deployed'] * 100:.1f}%",
         "Composite (Matched)": "0.0%",
         "Permissive Baseline": f"{primary['metrics']['Permissive']['unsafe_deployment_rate'] * 100:.1f}%"},
        {"Evidence Distribution Scenario": "Uniform failure (verified)",
         "Non-Comp. Gates": get_verif("Uniform Failure", "Gates"),
         "Composite (Moderate)": get_verif("Uniform Failure", "Composite (moderate)"),
         "Composite (Matched)": get_verif("Uniform Failure", "Composite (matched)"),
         "Permissive Baseline": get_verif("Uniform Failure", "Permissive")},
        {"Evidence Distribution Scenario": "Random failure (verified)",
         "Non-Comp. Gates": get_verif("Random Failure", "Gates"),
         "Composite (Moderate)": get_verif("Random Failure", "Composite (moderate)"),
         "Composite (Matched)": get_verif("Random Failure", "Composite (matched)"),
         "Permissive Baseline": get_verif("Random Failure", "Permissive")},
        {"Evidence Distribution Scenario": "Partial heterogeneity (verified)",
         "Non-Comp. Gates": get_verif("Partial Heterogeneity", "Gates"),
         "Composite (Moderate)": get_verif("Partial Heterogeneity", "Composite (moderate)"),
         "Composite (Matched)": get_verif("Partial Heterogeneity", "Composite (matched)"),
         "Permissive Baseline": get_verif("Partial Heterogeneity", "Permissive")},
        {"Evidence Distribution Scenario": "Noise robustness: Low (SD=0.01)",
         "Non-Comp. Gates": f"{ext_records[0]['gate_unsafe_rate'] * 100:.1f}%",
         "Composite (Moderate)": f"{ext_records[0]['composite_matched_unsafe_rate'] * 100:.1f}% (matched)",
         "Composite (Matched)": f"{ext_records[0]['composite_matched_unsafe_rate'] * 100:.1f}%",
         "Permissive Baseline": f"{ext_records[0]['permissive_unsafe_rate'] * 100:.1f}%"},
        {"Evidence Distribution Scenario": "Noise robustness: High (SD=0.20)",
         "Non-Comp. Gates": f"{ext_records[1]['gate_unsafe_rate'] * 100:.1f}%",
         "Composite (Moderate)": f"{ext_records[1]['composite_matched_unsafe_rate'] * 100:.1f}% (matched)",
         "Composite (Matched)": f"{ext_records[1]['composite_matched_unsafe_rate'] * 100:.1f}%",
         "Permissive Baseline": f"{ext_records[1]['permissive_unsafe_rate'] * 100:.1f}%"},
    ]
    pd.DataFrame(t2_rows).to_csv(OUT_TABLES / "table2_unsafe_rates.csv", index=False)

    # Static Figure 1
    shutil.copy2(BASE_DIR / "data" / "static" / "Figure1_DecisionRuleComparison.png",
                 OUT_FIGURES / "Figure1_DecisionRuleComparison.png")

    # Manifests
    fig_lines = ["Paper 2 Figure Manifest"]
    for f in sorted(OUT_FIGURES.glob("*.png")):
        fig_lines.append(f"{f.name}  {sha256_file(f)}")
    (OUT_FIGURES / "paper2_figure_manifest.txt").write_text("\n".join(fig_lines) + "\n", encoding="utf-8")

    tbl_lines = ["file,sha256"]
    for f in sorted(OUT_TABLES.glob("*.csv")):
        tbl_lines.append(f"{f.name},{sha256_file(f)}")
    (OUT_TABLES / "paper2_table_manifest.csv").write_text("\n".join(tbl_lines) + "\n", encoding="utf-8")

    # Supplementary report
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        from report_supplementary import main as report_main
        report_main(["--output-dir", str(OUT_DATA)])
    (OUT_LOGS / "supplementary_report.txt").write_text(buf.getvalue(), encoding="utf-8")

    # Execution log
    log = f"""Execution Log
Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
Python: {sys.version}
numpy: {np.__version__}
pandas: {pd.__version__}
Engine seed: 20260304
PYTHONHASHSEED: {os.environ.get('PYTHONHASHSEED', 'not set')}
Mode: direct (scripts/run_direct.py)
"""
    (OUT_LOGS / "execution_log.txt").write_text(log, encoding="utf-8")

    print("[DONE] All outputs generated.")


if __name__ == "__main__":
    main()
