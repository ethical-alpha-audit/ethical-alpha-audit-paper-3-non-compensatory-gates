# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

Reproducibility bundle for Paper 2 ("Non-Compensatory Decision Rules for Clinical AI Deployment Authorisation"). The pipeline is a deterministic Monte Carlo simulation study — every numerical claim in the manuscript must be regenerable byte-identically from `seed=20260304` and `PYTHONHASHSEED=0`. This is a research artifact, not a typical software project: code changes are scored against whether they preserve manuscript-exact outputs.

## Common commands

```bash
# Full pipeline (notebooks → manifest → validation → HTML export)
python reproduce_all.py

# Faster path that skips Jupyter (uses scripts/run_direct.py)
python reproduce_all.py --skip-notebooks

# Direct simulation only (no notebooks, no manifest regeneration)
python scripts/run_direct.py

# Specific stages
python -m src.run_verification            # Table C1 verification scenarios
python scripts/run_calibration_grid_2d.py # 5x5 calibration grid (Tables G1, G2, E1)
python scripts/run_counterhypothesis.py   # CH-1, CH-2, CH-3
python analysis/compute_crossover_ci.py   # CH-2 r* and bootstrap CI

# Validation (compares outputs to expected SHA-256 hashes)
python scripts/validate_outputs.py

# Regenerate the file manifest after intentional output changes
python scripts/hash_manifest.py

# Tests (structural only — does not run the simulation)
python -m pytest tests/ -v
```

`reproduce_all.py` sets `PYTHONHASHSEED` from `config/harness_settings.json` before invoking subprocesses; running individual scripts standalone may produce non-bit-identical outputs unless you export `PYTHONHASHSEED=0` first. `scripts/run_direct.py` does this itself.

## Architecture

### Two-layer pipeline

1. **Simulation layer (`src/`)** — generates the canonical 1,000-tool decision table. `src/run_simulation.py` is the engine: `simulate_portfolio` (latent safe/unsafe states + Beta-distributed evidence with heterogeneous gate-specific shifts for unsafe tools), then the three decision rules (`decide_noncomp_gates`, `decide_weighted_composite`, `decide_permissive`). `src/run_verification.py` and `src/run_calibration_sensitivity.py` are sibling drivers that reuse those primitives for the verification scope-condition scenarios and the calibration sweeps. Defaults live in `src/params_default.json`; loaded via `SimConfig` (a dataclass with explicit fields — when overriding via `asdict(SimConfig())`, tuple-typed fields like `override_disallowed_gates` and `unsafe_gate_profile` values must be re-tupleised before reconstruction, see `scripts/run_counterhypothesis.py:36`).

2. **Analysis layer (`analysis/`)** — pure post-processing on simulation outputs; never mutates them. `compute_crossover_ci.py` computes the cost-asymmetric crossover ratio `r*` with bootstrap CI by resampling the 1,000-tool portfolio (this is the source of truth for the manuscript's `r*=0.0155 (0.0106–0.0244)`).

### Notebook vs direct equivalence

The `notebooks/` (`01_primary_simulation` through `05_tables_and_summary`) and `scripts/run_direct.py` are functionally equivalent execution paths over the same engine. `reproduce_all.py` prefers notebooks when `nbclient` is installed and falls back to `run_direct.py` otherwise — both must produce the same outputs. If you change engine behaviour, update both paths (or verify the notebooks re-pick the engine change unchanged) before regenerating the manifest.

### Determinism contract

- All RNG flows through `numpy.random.default_rng(seed)`; do not introduce `random.*`, `np.random` globals, or any external RNG.
- All iteration over dict-like data is over sorted keys; preserve this when adding new aggregation code.
- CSVs are written with `lineterminator="\n"`; JSON with `newline="\n"` and `indent=2`. Both are required for cross-platform byte-identical output on Windows.
- After any intended output change: run `python scripts/hash_manifest.py` to regenerate `MANIFEST.sha256`, then `python scripts/validate_outputs.py` to confirm. `config/expected_outputs.json` carries per-file `hash_mode` (`strict` vs `advisory`) — strict mismatches fail validation, advisory ones warn.

### Trace map

`config/trace_map.json` maps every output file to (a) the notebook that produces it and (b) the RTM target IDs (D-/Q-/F-/T-) used in the manuscript and `docs/claim_traceability.md`. Use this as the index when a reviewer asks "where does value X come from" or when adding a new output: register it here and in `config/expected_outputs.json` and `config/notebook_plan.json`, or it will be missed by the validator.

## Conventions specific to this repo

- **Manuscripts and PDFs are gitignored on purpose.** `inputs/*.docx`, `inputs/*.pdf`, and top-level `*.docx`/`*.doc` must stay on disk (needed for PowerShell readiness gates and Jupyter workflows) but never enter git history. See the no-commit-manuscripts policy block in `.gitignore`. Do not stage these files even if `git add` doesn't complain about them — verify with `git status` after staging.
- **`canonical_documents.yaml` tracks document provenance**, including SHA-256 hashes and deployment status for each manuscript/supplementary axis. Edits to manuscript files should be reflected here.
- **`outputs/` is committed.** Pre-generated outputs are part of the artifact; do not assume regeneration is required before working with them. If you regenerate, expect a clean diff (or no diff) — anything else means the determinism contract was broken.
- **Tests are structural, not numerical.** `tests/` only verifies that expected files exist; numerical correctness is enforced by `validate_outputs.py` against `MANIFEST.sha256` + `config/expected_outputs.json`.
