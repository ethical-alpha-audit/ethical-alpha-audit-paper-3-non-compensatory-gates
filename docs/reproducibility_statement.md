# Reproducibility Statement

## How to reproduce

From the repository root, with dependencies installed per `requirements.txt`:

```bash
python reproduce_all.py
```

This executes 5 notebooks in sequence (or falls back to direct script execution if Jupyter is unavailable), computes SHA-256 hashes of all output files, and validates them against `config/expected_outputs.json`. A passing result (`ALL STEPS PASSED`) confirms reproduction.

## Determinism guarantees

- `PYTHONHASHSEED=0` enforced by harness before any execution
- `numpy.random.default_rng(seed=20260304)` for all stochastic operations
- `matplotlib.use('Agg')` for headless rendering (set in engine code)
- All CSV output uses pandas default float precision with deterministic column ordering
- All JSON output uses `indent=2` with `default=str` for consistent serialisation
- Single-threaded execution throughout (no parallelism)
- No network dependencies; all computation uses local code and synthetic data

## Dual hash policy

- **STRICT**: CSV, JSON, and text outputs must match expected SHA-256 exactly. A mismatch is a validation failure.
- **ADVISORY**: PNG and PDF figures are logged but mismatches produce warnings, not failures. Matplotlib rendering may produce slightly different bytes across platforms.

## Validation without execution

```bash
python scripts/validate_outputs.py
```

Requires only Python stdlib. Verifies checked-in outputs match expected hashes.

## Known annotations

- **A-01**: Permissive rate at noise SD=0.01 computes 2.0% vs manuscript 1.9% (1-tool boundary)
- **A-02**: Threshold multipliers 0.60–0.65 produce 0.1–0.2% non-zero gate leakage
- **A-03**: Epic case NaN RuntimeWarning is cosmetic; output is correct
- **A-04**: Figure hashes are platform-dependent (ADVISORY policy)
