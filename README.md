# Non-Compensatory Governance Gates: Simulation Study

> **Paper 2** of the Ethical Alpha Audit research programme
>
> Author: Walter Brown — Ethical Alpha Audit Ltd
> ORCID: [0000-0002-6050-8522](https://orcid.org/0000-0002-6050-8522)

## Reviewer quick validation (no execution required)

```bash
python scripts/validate_outputs.py
```

**Expected result:** `VALIDATION PASSED`

This checks every output file against its pinned SHA-256 digest. No notebook execution, no dependencies beyond Python stdlib. A passing result confirms the checked-in outputs are byte-identical to those produced by the deterministic pipeline.

**To re-execute the full pipeline** (requires dependencies):

```bash
pip install -r requirements.txt
python reproduce_all.py
```

## What this repository reproduces

Monte Carlo simulation comparing three governance decision rules applied to 1,000 simulated clinical AI tools with heterogeneous evidence profiles across five governance domains.

| Result | Gates | Composite (Moderate) | Permissive |
|--------|:-----:|:--------------------:|:----------:|
| Deploy rate | 28.5% | 62.7% | 76.0% |
| Unsafe deploy rate | 0.0% | 0.9% | 2.2% |
| 95% CI | [0.0%, 0.0%] | [0.4%, 1.6%] | [1.3%, 3.2%] |

Additionally: three verification simulations (uniform, random, partial heterogeneity), threshold sensitivity (60%–140%), noise robustness (SD 0.01–0.20), Epic Sepsis Model case scenario, portfolio composition sensitivity, and unsafe probability sensitivity.

## Repository structure

```
src/                Simulation engine (5 files, unmodified from experimental authority)
config/             Determinism settings, execution plan, expected output hashes, trace map
data/static/        Manuscript Figure 1 schematic (pre-rendered, not generated)
notebooks/          5 Jupyter notebooks (ordered pipeline)
scripts/            Execution harness (notebook runner, hash validator, HTML export)
outputs/            Generated figures, tables, data, and logs (hash-locked)
tests/              Structural and reproducibility tests
docs/               Methods note, provenance, reproducibility statement
```

## Notebook pipeline

| # | Notebook | Produces |
|---|----------|----------|
| 1 | `01_primary_simulation.ipynb` | Primary simulation, metrics, bootstrap CIs, Epic case, figures 1–4 |
| 2 | `02_sensitivity_and_noise.ipynb` | Threshold sensitivity, noise robustness, figures 5–6 |
| 3 | `03_verification_simulations.ipynb` | 3 scope-condition verifications, comparison figure |
| 4 | `04_calibration_sensitivity.ipynb` | Portfolio and unsafe probability sensitivity sweeps |
| 5 | `05_tables_and_summary.ipynb` | Manuscript Tables 1–2, manifests, supplementary report |

## Determinism

All results are deterministic given seed 20260304 and pinned dependencies. `PYTHONHASHSEED=0` is enforced by the harness. Re-execution from identical inputs produces identical CSV/JSON outputs. Figure hashes may vary across platforms (matplotlib rendering); these are validated under an advisory policy.

## License

MIT License. See [LICENSE](LICENSE).
