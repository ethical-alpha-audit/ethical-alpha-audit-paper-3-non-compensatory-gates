# Provenance

## Engine

All five engine files in `src/` are byte-identical copies of the experimental scientific authority (`noncomp_gates_simulation_v3.zip`). They have not been modified in any way.

- `run_simulation.py` — Primary Monte Carlo simulation (926 lines)
- `run_verification.py` — Verification simulations for scope conditions (424 lines)
- `run_calibration_sensitivity.py` — Portfolio and probability sensitivity sweeps (235 lines)
- `report_supplementary.py` — Aggregated supplementary results report (118 lines)
- `params_default.json` — Canonical parameter configuration (seed: 20260304)

## Engine file hashes (I2 originals)

```
6bea7921709f35554f43a1c46e50f02d3035effe4ecdf90dd082da7ca4ae2dec  run_simulation.py
abde196287dff231dd636cbbc2d5f5f149aa8f56843e2f2dba6b4bfcff89602a  run_verification.py
09e6e156e1a522905f970e8185a348d44e6c20c066a1a2260aa4b18787ac10c0  run_calibration_sensitivity.py
7396f34f96bea56021ff0f397e9efe1864050a26abe86a32ade57271a33d58ea  report_supplementary.py
ed8a57ecc3711607b335aa79abf0059e27dcb67716633fc0f2eb0913e774dd9d  params_default.json
```

## Static asset

- `data/static/Figure1_DecisionRuleComparison.png` — Manuscript Figure 1 (conceptual schematic, not computationally generated). Byte-identical copy from the manuscript bundle.

## Parameter authority

`src/params_default.json` is the sole parameter authority. All simulation parameters, thresholds, weights, and override configuration are sourced from this file. No parameters are hardcoded in notebooks.

## Canonical authority decisions

- **Engine**: I2 (`noncomp_gates_simulation_v3`) is the sole computational authority
- **Manuscript**: I1 (`Paper_2_FINAL`) is the sole truth target for what must be reproduced
- **Exemplar**: I3 (`ethical-alpha-audit-paper-4-historical-replay-main`) provided structural patterns only; no data, engine code, or numerical outputs were imported
