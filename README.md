# Reproducibility bundle — Paper 2 v3.3

**Title:** Non-Compensatory Decision Rules for Clinical Artificial Intelligence Deployment Authorisation: A Theory-Testing Monte Carlo Simulation of Scope Conditions and Cost-Asymmetric Loss

**Article type:** Simulation Study  |  **Target journal:** JMIR Medical Informatics

This bundle contains the full code, configuration, and pre-generated outputs needed to reproduce all numerical values in the manuscript. The pipeline is deterministic: re-execution from identical seed and configuration produces byte-identical outputs.

---

## 1. Repository layout

```
.
├── README.md                              ← this file
├── requirements.txt                       ← pinned Python dependencies
├── runtime.txt                            ← Python version (3.11)
├── environment.yml                        ← conda environment specification
├── environment.lock                       ← exact lock file
├── VERSION                                ← bundle version string
├── CITATION.cff                           ← citation metadata
├── LICENSE                                ← MIT license
├── MANIFEST.sha256                        ← SHA-256 manifest of all repository files
│
├── src/                                   ← simulation engine
│   ├── run_simulation.py                  ← primary-model simulation
│   ├── run_verification.py                ← analytical scope-condition verification
│   ├── run_calibration_sensitivity.py     ← 1-D calibration sensitivity sweeps
│   ├── report_supplementary.py            ← supplementary report generation
│   └── params_default.json                ← default simulation parameters
│
├── analysis/                              ← deterministic post-processing
│   └── compute_crossover_ci.py            ← CH-2 crossover ratio + bootstrap CI
│
├── scripts/                               ← workflow drivers
│   ├── run_direct.py                      ← run primary simulation directly
│   ├── run_calibration_grid_2d.py         ← 5x5 calibration grid (CH-2 grid sensitivity)
│   ├── run_counterhypothesis.py           ← CH-1 / CH-2 / CH-3 counter-hypothesis runs
│   ├── validate_outputs.py                ← deterministic-output validation
│   └── hash_manifest.py                   ← regenerate SHA-256 manifest
│
├── config/                                ← named configuration files
├── inputs/                                ← input data files (none required for primary model)
├── outputs/                               ← pre-generated simulation outputs (committed)
│   ├── data/                              ← primary-model simulation outputs
│   │   └── simulation_outputs.csv         ← primary-model decision-vectors (1,000 tools)
│   ├── tables/                            ← rendered tables
│   ├── figures/                           ← rendered figures
│   ├── grid_2d/                           ← 5x5 calibration grid outputs
│   │   ├── calibration_grid_2d.csv        ← per-grid-point metrics
│   │   ├── table_G1_gate_unsafe_grid.csv  ← Table G1 (manuscript)
│   │   ├── table_G2_composite_unsafe_grid.csv  ← Table G2 (manuscript)
│   │   └── summary_stats.json             ← summary statistics (Table E1)
│   ├── counter_hypothesis/                ← CH-1, CH-2, CH-3 outputs
│   │   ├── ch1_high_noise_low_danger.json
│   │   ├── ch2_cost_asymmetric_loss.csv   ← Table CH-2 (manuscript)
│   │   ├── ch2_summary.json
│   │   ├── ch3_uniform_high_quality.json
│   │   └── counter_hypothesis_summary.json
│   ├── derived/                           ← deterministic post-processing outputs
│   │   └── ch2_crossover_ci.json          ← r* point estimate + bootstrap 95% CI
│   └── logs/                              ← run logs
│
├── tests/                                 ← unit tests
├── notebooks/                             ← exploratory notebooks
├── docs/                                  ← additional documentation
├── repro_manifest.json                    ← reproducibility manifest
└── reproduce_all.py                       ← single-command re-execution driver
```

---

## 2. Quick start (minimal reproduction)

### 2.1 Environment

```bash
python -m venv .venv
source .venv/bin/activate           # POSIX
# .venv\Scripts\activate            # Windows
pip install -r requirements.txt
```

Python 3.11 required. Core dependencies: numpy, pandas, matplotlib.

### 2.2 Reproduce all manuscript values

```bash
python reproduce_all.py
```

This single command regenerates all primary-model outputs, calibration grid, counter-hypothesis runs, and the deterministic post-processing analysis. Total runtime on a modern laptop: under ten minutes.

### 2.3 Reproduce specific results

| Manuscript element | Command | Output file |
|---|---|---|
| Primary heterogeneous-model results (28.5% gate deployment, 0.9% unsafe rate, 1.4% contamination) | `python scripts/run_direct.py` | `outputs/data/simulation_outputs.csv`, `outputs/data/metrics_summary.json` |
| Threshold sensitivity, noise robustness | `python scripts/run_direct.py` | `outputs/data/sensitivity_thresholds.csv`, `outputs/data/sensitivity_noise.csv` |
| Verification simulations (uniform / random / partial heterogeneity; Table C1) | `python -m src.run_verification` | `outputs/data/verification_summary.csv` |
| 5x5 calibration grid (Tables G1, G2, E1) | `python scripts/run_calibration_grid_2d.py` | `outputs/grid_2d/*.csv`, `outputs/grid_2d/summary_stats.json` |
| Counter-hypothesis CH-1, CH-2, CH-3 (Tables CH-1, CH-2, CH-3) | `python scripts/run_counterhypothesis.py` | `outputs/counter_hypothesis/*.json`, `outputs/counter_hypothesis/ch2_cost_asymmetric_loss.csv` |
| Cost-asymmetric crossover r* and 95% CI | `python analysis/compute_crossover_ci.py` | `outputs/derived/ch2_crossover_ci.json` |

### 2.4 Validate determinism

```bash
python scripts/validate_outputs.py
```

Re-execution from identical seed (20260304) produces byte-identical outputs. The validation script regenerates outputs and compares them against the SHA-256 manifest in `MANIFEST.sha256`.

---

## 3. Pipeline architecture

The analytical pipeline has two layers:

### 3.1 Simulation layer (`src/`)

The primary-model simulation generates the canonical 1,000-tool decision-vector table `outputs/data/simulation_outputs.csv` containing latent safety states, observed evidence scores per governance domain, and deployment decisions under each rule (non-compensatory gates, composite-matched, composite-moderate, composite-zero-imputation, permissive baseline). Random number generation is seeded (default `seed=20260304`) and uses `numpy.random.default_rng`.

### 3.2 Analysis layer (`analysis/`)

Deterministic post-processing operates only on the simulation-layer outputs and never modifies them. Currently includes:

**`compute_crossover_ci.py`** — computes the cost-asymmetric expected-loss crossover ratio `r*` between non-compensatory gates and weighted-composite-moderate scoring, with bootstrap 95% confidence interval, from the primary-model simulation output.

#### Method (cost-asymmetric crossover and 95% CI)

For each decision rule, expected per-tool loss is computed as

```
L = c_FP * P(deploy & unsafe) + c_FN * P(~deploy & safe)
```

For each cost ratio `r = c_FN / c_FP` in `{0.01, 0.10, 0.50, 1, 2, 5, 10, 50, 100}`, the loss difference `L(gates) - L(composite_moderate)` is computed. The crossover `r*` is located by log-linear interpolation between the first bracketing pair of cost ratios where the difference changes sign.

Bootstrap 95% CI: the underlying primary-model 1,000-tool portfolio is resampled with replacement (seed = 20260304, 1,000 resamples), and the crossover is re-computed for each resample. The 2.5th and 97.5th percentiles of the bootstrap distribution define the 95% CI. Resamples that produce no sign change in the tested cost-ratio range are excluded from CI computation; the converged-resample count is reported.

#### Reproducible result

```json
{
  "r_star_point": 0.0155,
  "ci_low":  0.0106,
  "ci_high": 0.0244,
  "ci_level": 0.95,
  "n_bootstrap_total":     1000,
  "n_bootstrap_converged":  977,
  "seed": 20260304
}
```

These values populate the manuscript Methods §"Counter-hypothesis scope conditions", Results §"CH-2: Cost-asymmetric expected-loss analysis", Limitations, and Multimedia Appendix 2 §F.

---

## 4. Mapping: manuscript values → repository outputs

| Manuscript value | Repository output |
|---|---|
| 28.5% gate deployment rate | `outputs/data/metrics_summary.json` |
| 0.9% (0.4–1.6%) unsafe deployment rate, composite-moderate | `outputs/data/metrics_summary.json` |
| 1.4% contamination rate, composite-moderate | `outputs/data/metrics_summary.json` |
| 2.2% unsafe deployment rate, permissive baseline | `outputs/data/metrics_summary.json` |
| Threshold sensitivity zero-unsafe across multiplier range | `outputs/data/sensitivity_thresholds.csv` |
| Noise robustness zero-unsafe across SD range | `outputs/data/sensitivity_noise.csv` |
| Uniform / random / partial verification (Table C1) | `outputs/data/verification_summary.csv` |
| Table G1 (gate unsafe-rate grid) | `outputs/grid_2d/table_G1_gate_unsafe_grid.csv` |
| Table G2 (composite-moderate unsafe-rate grid) | `outputs/grid_2d/table_G2_composite_unsafe_grid.csv` |
| Table E1 calibration-grid summary statistics | `outputs/grid_2d/summary_stats.json` |
| Table CH-1 (high-noise + low-danger; FN gap 75.5 vs 46.2 = +29.3 pp) | `outputs/counter_hypothesis/ch1_high_noise_low_danger.json` |
| Table CH-2 (cost-asymmetric loss curves) | `outputs/counter_hypothesis/ch2_cost_asymmetric_loss.csv` |
| Crossover r* = 0.015 (95% CI 0.011–0.024) | `outputs/derived/ch2_crossover_ci.json` |
| Table CH-3 (near-uniform high-quality; gates 4.0% vs composite-moderate 12.3%) | `outputs/counter_hypothesis/ch3_uniform_high_quality.json` |
| Decomposition robustness (4.0%–7.1% range) | `outputs/data/verification_summary.csv` |
| Epic Sepsis case scenario | `outputs/data/epic_case_outputs.csv` |

---

## 5. Configuration

Primary-model defaults are specified in `src/params_default.json` and reproduced in the manuscript Methods Table "Model specification at a glance". Key parameters:

| Parameter | Default | Manuscript reference |
|---|---|---|
| `n_tools` | 1,000 | Methods §Study design |
| `seed` | 20260304 | Methods §Study design |
| `n_bootstrap` | 1,000 (over tool resampling) | Methods §Outcome measures |
| `p_high_risk` | 0.30 | Methods §Portfolio generation |
| `p_unsafe_high` | 0.35 (modelling assumption) | Methods §Portfolio generation, §Calibration and realism |
| `p_unsafe_standard` | 0.15 (modelling assumption) | Methods §Portfolio generation |
| `obs_noise_sd` | 0.06 | Methods §Sensitivity scenarios |
| `thresholds_high (G1 / G2–G5)` | 0.65 / 0.60 | Methods §Governance decision rules |
| `thresholds_standard (G1 / G2–G5)` | 0.55 / 0.50 | Methods §Governance decision rules |
| `override_prob` | 0.10 (Gates 2–4) | Methods §Governance decision rules |
| `composite weights (G1 : G2 : G3 : G4 : G5)` | 0.30 : 0.15 : 0.15 : 0.15 : 0.25 | Methods §Governance decision rules |
| `permissive_min_gates_passed` | 3 of 5 | Methods §Governance decision rules |

---

## 6. Determinism guarantees

1. All random number generation uses `numpy.random.default_rng(seed)` with seed 20260304.
2. All ordered iteration is over sorted keys.
3. All numerical outputs are written with fixed-precision rounding for stable comparison.
4. Two re-executions from the same source state produce byte-identical outputs (validated by `scripts/validate_outputs.py` against `MANIFEST.sha256`).

---

## 7. License and citation

License: MIT (see `LICENSE`).

Citation: see `CITATION.cff`.

---

## 8. Contact

Walter Brown · walter.brown@ethicalalphaaudit.com · Ethical Alpha Audit Ltd, London, UK · ORCID: 0000-0002-6050-8522
