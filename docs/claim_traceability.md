# Claim Traceability Matrix

**Repo:** ethical-alpha-audit-paper-2-threshold-justification  
**Updated:** 2026-04-12 (engineer remediation session)  
**Source manuscript:** `inputs/manuscript.pdf` (JMIR Medical Informatics submission draft)  
**Supplementary:** `inputs/supplementary.pdf`  
**Claims:** 22 | **Verified:** traceability to repo artifacts (notebooks / `src/` / `outputs/`)

RTM targets in `config/trace_map.json` use manuscript internal IDs (D-01, Q-01, F-01, T-01, …). This document adds **P2-Cxx** IDs for portfolio QA.

---

## Enumeration

**CLAIM EXTRACTION COMPLETE: 22 claims identified for P2.**

| Claim ID | Manuscript-grounded statement (paraphrase) | Primary evidence (repo) | Notebook / module | Key outputs |
|----------|--------------------------------------------|-------------------------|-------------------|-------------|
| P2-C01 | Monte Carlo simulation of 1,000 clinical AI tools with latent safety state and five-domain evidence; theory-testing frame | Engine config `n_tools`, design in Methods | `notebooks/01_primary_simulation.ipynb`, `src/run_simulation.py` | `outputs/data/simulation_outputs.csv`, `outputs/data/metrics_summary.json` |
| P2-C02 | Portfolio mix 30% high-risk / 70% standard-risk reflects institutional composition narrative | `p_high_risk`, risk tiers in config | `src/run_simulation.py`, `src/params_default.json` | `metrics_summary.json` → `config` |
| P2-C03 | Latent unsafe probabilities 0.35 (high-risk) and 0.15 (standard-risk) | `p_unsafe_high`, `p_unsafe_standard` | `src/run_simulation.py` | `simulation_outputs.csv`, `metrics_summary.json` |
| P2-C04 | Non-compensatory gates: five domains, risk-tiered thresholds; override on gates 2–4 at modelled invocation rate | Threshold + override parameters | `src/run_simulation.py` | `metrics_summary.json` (override rates) |
| P2-C05 | Weighted composite at matched threshold (to gate deploy rate) and moderate threshold (~2.2× gate rate, capped) | `set_threshold_to_match_rate`, 2.2× rule | `src/run_simulation.py`, `scripts/run_direct.py` | `metrics_summary.json` → `composite_thresholds` |
| P2-C06 | Permissive baseline: majority rule (≥3 of 5 gates) | `decide_permissive` | `src/run_simulation.py` | `simulation_outputs.csv`, metrics |
| P2-C07 | Primary heterogeneous model: gates ~28.5% deployment; **zero** unsafe deployments; moderate composite unsafe deployment ~0.9% with CI; ~1.4% unsafe among deployed | Point estimates + bootstrap | `01_primary_simulation.ipynb` | `metrics_summary.json`, figures |
| P2-C08 | Permissive baseline ~2.2% unsafe deployment rate under primary model | Metrics column `Permissive` | `01_primary_simulation.ipynb` | `metrics_summary.json`, `outputs/tables/table2_unsafe_rates.csv` |
| P2-C09 | Threshold sensitivity: multipliers 60–140% of default (17 steps); gate safety under primary model | Sweep implementation | `02_sensitivity_and_noise.ipynb` | `outputs/data/sensitivity_thresholds.csv`, `fig5_*` |
| P2-C10 | Noise robustness: observation SD 0.01–0.20 (15 steps in engine); matched composite calibration at each level | `noise_robustness` | `02_sensitivity_and_noise.ipynb` | `outputs/data/sensitivity_noise.csv`, `fig6_*` |
| P2-C11 | Extended noise rows (low/high SD) for Table 2 noise section | `noise_extended` generation | `02_sensitivity_and_noise.ipynb`, `scripts/run_direct.py` | `outputs/data/noise_extended.csv` |
| P2-C12 | Verification scenarios: uniform failure, random failure, partial heterogeneity — rates vs composite (moderate/matched) and permissive | Scenario definitions | `03_verification_simulations.ipynb`, `src/run_verification.py` | `verification_summary.csv`, `verification_results.json`, `fig_verification_*` |
| P2-C13 | Uniform failure: gate advantage vs moderate composite collapses toward matched comparison (manuscript Table 1–2 narrative) | Scenario outputs | `03_verification_simulations.ipynb` | `verification_summary.csv`, `table1_scope_conditions.csv` |
| P2-C14 | Random failure: small non-zero unsafe rate under gates; higher under moderate composite | Scenario outputs | `03_verification_simulations.ipynb` | `verification_summary.csv`, tables |
| P2-C15 | Partial heterogeneity: non-zero gate unsafe rate; composite moderate higher | Scenario outputs | `03_verification_simulations.ipynb` | `verification_summary.csv`, tables |
| P2-C16 | Calibration sensitivity: portfolio composition and unsafe-probability sweeps (supplementary / robustness narrative) | Formal axes in appendix reference | `04_calibration_sensitivity.ipynb`, `src/run_calibration_sensitivity.py` | `calibration_portfolio.csv`, `calibration_unsafe_prob.csv`, `fig_portfolio_*`, `fig_unsafe_prob_*` |
| P2-C17 | Table 1: scope-condition summary (mechanism column aligned to manuscript) | Assembled from primary + verification | `05_tables_and_summary.ipynb` | `outputs/tables/table1_scope_conditions.csv` |
| P2-C18 | Table 2: unsafe deployment rates across scenarios and rules | Joins primary metrics + verification + noise | `05_tables_and_summary.ipynb` | `outputs/tables/table2_unsafe_rates.csv` |
| P2-C19 | Epic Sepsis case scenario: under gates, fails all five domains with transparent domain-level refusal | `epic_case_row`, decisions | `01_primary_simulation.ipynb` | `epic_case_outputs.csv`, `fig4_epic_case.*` |
| P2-C20 | Bootstrap 95% CIs (1,000 resamples) for rates | `bootstrap_ci`, `n_bootstrap` | `src/run_simulation.py` | `metrics_summary.json`, `verification_results.json` |
| P2-C21 | Reproducibility: single-command pipeline and manifest validation | Harness | `reproduce_all.py`, `scripts/validate_outputs.py`, `scripts/hash_manifest.py` | `logs/actual_manifest.json`, `config/expected_outputs.json` |
| P2-C22 | Aggregated supplementary numeric report (appendix alignment) | Reporter | `src/report_supplementary.py` | `outputs/logs/supplementary_report.txt` |

### Manuscript-only / sibling-repo claims (no P2 code path)

The manuscript cites the **companion historical replay** (Core-12, expanded cohort, control devices). Those numerical results are produced in **P4** (`ethical-alpha-audit-paper-4-historical-replay`), not in this repository. Treat as **cross-paper traceability**; do not infer P2 outputs validate P4 metrics.

---

## RTM crosswalk (selected)

| P2 claim | trace_map.json RTM targets (examples) |
|----------|--------------------------------------|
| P2-C01, P2-C07 | D-01, D-02, Q-01–Q-10, F-02–F-05 |
| P2-C09 | D-04, Q-27, F-06 |
| P2-C10, P2-C11 | D-05, Q-25, Q-26, F-07 |
| P2-C12–P2-C15 | D-06, D-07, Q-11–Q-24, F-08 |
| P2-C16 | D-08, D-09, Q-30, Q-31, F-09, F-10 |
| P2-C17 | T-01 |
| P2-C18 | T-02 |
| P2-C19 | D-03, Q-28, Q-29, F-05 |
| P2-C22 | supplementary log (no RTM id) |

---

## Status

All listed claims are **grounded** in `inputs/manuscript.pdf` and mapped to **existing** pipeline artifacts. Discrepancies between manuscript prose and regenerated numbers should trigger **escalation**, not silent retuning of simulation logic.
