#!/usr/bin/env python3
"""
analysis/compute_crossover_ci.py

Deterministic post-processing of primary-heterogeneous-model simulation outputs.
Computes the cost-asymmetric expected-loss crossover ratio r* between
non-compensatory gates and weighted-composite-moderate scoring, with
bootstrap 95% confidence interval.

This module:
  - loads the primary-model decision-vectors from outputs/data/portfolio.csv
  - computes expected per-tool loss L = c_FP * P(deploy & unsafe) + c_FN * P(~deploy & safe)
    for each rule at each cost ratio r = c_FN / c_FP in {0.01, 0.1, 0.5, 1, 2, 5, 10, 50, 100}
  - identifies the crossover r* by log-linear interpolation between bracketing grid points
  - bootstraps the crossover by resampling tools (1,000 resamples) at fixed seed 20260304
  - writes outputs/derived/ch2_crossover_ci.json

The simulation outputs themselves are NOT modified; this is a deterministic
post-processing step.

Usage:
    python analysis/compute_crossover_ci.py

Inputs (read-only):
    outputs/data/portfolio.csv          (primary-model simulation output;
                                         contains columns deploy_gate,
                                         deploy_composite_mean_moderate, unsafe_true)

Outputs (written):
    outputs/derived/ch2_crossover_ci.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

# ── Configuration (deterministic) ──────────────────────────────────────────
SEED            = 20260304
N_BOOTSTRAP     = 1000
COST_RATIOS     = (0.01, 0.10, 0.50, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0)

ROOT            = Path(__file__).resolve().parent.parent
INPUT_CSV       = ROOT / "outputs" / "data" / "simulation_outputs.csv"
OUTPUT_JSON     = ROOT / "outputs" / "derived" / "ch2_crossover_ci.json"

DEPLOY_GATE_COL = "deploy_gate"
# In simulation_outputs.csv, deploy_composite_mean is the moderate-threshold composite
# (calibrated to 2.2x gate deployment rate; produces ~62.7% deployment rate with
# the default heterogeneous-model parameters and seed 20260304).
DEPLOY_CM_COL   = "deploy_composite_mean"
UNSAFE_COL      = "unsafe_true"


def _expected_loss(deploy: np.ndarray, unsafe: np.ndarray,
                   c_fp: float, c_fn: float) -> float:
    """Expected per-tool loss = c_fp*P(deploy & unsafe) + c_fn*P(~deploy & safe)."""
    n = len(deploy)
    fp = float((deploy & unsafe).sum() / n)
    fn = float(((~deploy) & (~unsafe)).sum() / n)
    return c_fp * fp + c_fn * fn


def _crossover_log_linear(ratios: tuple, diffs: np.ndarray) -> float | None:
    """Find r* where loss(gates) = loss(comp-mod), via log-linear interpolation
    between the first sign-change in diffs = L_gates - L_comp_mod."""
    for i in range(len(ratios) - 1):
        if diffs[i] < 0 and diffs[i + 1] > 0:
            x0, x1 = np.log10(ratios[i]), np.log10(ratios[i + 1])
            y0, y1 = diffs[i], diffs[i + 1]
            return float(10 ** (x0 - y0 * (x1 - x0) / (y1 - y0)))
    return None


def _crossover_for_indices(deploy_g: np.ndarray, deploy_cm: np.ndarray,
                           unsafe: np.ndarray) -> float | None:
    diffs = np.array([
        _expected_loss(deploy_g,  unsafe, 1.0, r)
      - _expected_loss(deploy_cm, unsafe, 1.0, r)
        for r in COST_RATIOS
    ])
    return _crossover_log_linear(COST_RATIOS, diffs)


def main() -> None:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"Required simulation output not found: {INPUT_CSV}\n"
            f"Run `python reproduce_all.py` first to generate primary-model outputs."
        )

    df = pd.read_csv(INPUT_CSV)
    for col in (DEPLOY_GATE_COL, DEPLOY_CM_COL, UNSAFE_COL):
        if col not in df.columns:
            raise KeyError(
                f"Expected column '{col}' missing from {INPUT_CSV}.\n"
                f"Available columns: {list(df.columns)}"
            )

    deploy_g  = df[DEPLOY_GATE_COL].to_numpy().astype(bool)
    deploy_cm = df[DEPLOY_CM_COL].to_numpy().astype(bool)
    unsafe    = df[UNSAFE_COL].to_numpy().astype(bool)
    n         = len(df)

    # Point estimate
    r_star_point = _crossover_for_indices(deploy_g, deploy_cm, unsafe)
    if r_star_point is None:
        raise RuntimeError(
            f"No finite crossover ratio found in tested range "
            f"[{COST_RATIOS[0]}, {COST_RATIOS[-1]}] on point estimate."
        )

    # Bootstrap 95% CI
    rng = np.random.default_rng(SEED)
    crossings = []
    for _ in range(N_BOOTSTRAP):
        idx = rng.integers(0, n, n)
        r_b = _crossover_for_indices(deploy_g[idx], deploy_cm[idx], unsafe[idx])
        if r_b is not None:
            crossings.append(r_b)

    crossings = np.array(crossings)
    ci_low, ci_high = np.percentile(crossings, [2.5, 97.5])

    output = {
        "r_star_point":           round(float(r_star_point), 4),
        "ci_low":                 round(float(ci_low),       4),
        "ci_high":                round(float(ci_high),      4),
        "ci_level":               0.95,
        "n_bootstrap_total":      N_BOOTSTRAP,
        "n_bootstrap_converged":  int(len(crossings)),
        "cost_ratios_tested":     list(COST_RATIOS),
        "method": (
            "Bootstrap percentile 95% confidence interval for the cost-asymmetric "
            "expected-loss crossover ratio r* between non-compensatory gates and "
            "weighted-composite-moderate scoring. Expected per-tool loss for each "
            "decision rule is computed as L = c_FP * P(deploy & unsafe) + "
            "c_FN * P(~deploy & safe). For each cost ratio r = c_FN / c_FP in "
            "{0.01, 0.10, 0.50, 1, 2, 5, 10, 50, 100}, the loss difference "
            "L(gates) - L(composite_moderate) is computed; the crossover r* is "
            "located by log-linear interpolation between the first bracketing pair "
            "of cost ratios where the difference changes sign. Bootstrap resamples "
            "the underlying primary-model 1,000-tool portfolio with replacement "
            "(seed = 20260304, 1,000 resamples) and re-computes the crossover for "
            "each resample. The 2.5th and 97.5th percentiles of the bootstrap "
            "distribution define the 95% CI. Resamples that produce no sign change "
            "in the tested range are excluded from the CI computation; "
            "n_bootstrap_converged reports the number of usable resamples."
        ),
        "input_file":             str(INPUT_CSV.relative_to(ROOT)),
        "seed":                   SEED,
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))
    print(f"\nWrote: {OUTPUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
