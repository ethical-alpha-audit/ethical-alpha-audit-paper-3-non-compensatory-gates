# Non-Compensatory Governance Gates: Simulation Code

Reference implementation for:

> Brown W. Operationalizing non-compensatory governance gates: A theory-testing
> simulation study of clinical AI deployment decisions. *JMIR Medical Informatics*. 2026.
> (Under review.)

## Quick Start

```bash
pip install -r requirements.txt
python run_simulation.py                   # Primary simulation
make supplementary                         # All supplementary analyses
python report_supplementary.py             # Combined results report
```

All outputs are saved to `./outputs/`.

## Repository Structure

```
gates_simulation/
├── run_simulation.py               # Primary simulation (paper Tables 1-2, Figures 1-6)
├── run_verification.py             # Verification simulations for analytical scope conditions
├── run_calibration_sensitivity.py  # Calibration sensitivity analyses
├── report_supplementary.py         # Combined supplementary results report
├── params_default.json             # Default parameter configuration
├── requirements.txt                # Python dependencies
├── Makefile                        # Convenience targets
├── LICENSE                         # MIT License
└── README.md                       # This file
```

## Primary Simulation

The primary simulation implements Monte Carlo comparison of three governance decision
rules applied to 1000 simulated clinical AI tools with heterogeneous evidence profiles.

### Key Results (Primary Heterogeneous Model)

| Method | Deploy Rate | Unsafe Deploy Rate | 95% CI |
|--------|:-:|:-:|:-:|
| Non-compensatory gates | 28.5% | 0.0% | [0.0%, 0.0%] |
| Composite (matched) | 28.5% | 0.0% | [0.0%, 0.0%] |
| Composite (moderate) | 62.7% | 0.9% | [0.4%, 1.6%] |
| Permissive baseline | 76.0% | 2.2% | [1.3%, 3.2%] |

## Supplementary Simulations

### Verification Simulations

| Scenario | Gates | Composite (moderate) | Permissive |
|----------|:-:|:-:|:-:|
| Uniform failure | 0.0% | 1.2% | 4.0% |
| Random failure | 0.9% | 6.1% | 8.6% |
| Partial heterogeneity | 0.8% | 7.4% | 9.4% |

### Calibration Sensitivity

- **Portfolio composition** (10/90 to 50/50): Gates 0.0% across all. Robust.
- **Unsafe probability** (±30%): Gates 0.0% in 4/5 conditions. Robust.

## Reproducibility

All results are deterministic given the default seed (20260304).

```bash
make all    # Reproduce everything
```

## License

MIT License. See [LICENSE](LICENSE).
