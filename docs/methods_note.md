# Methods Note

## Simulation Architecture

The simulation generates a portfolio of 1,000 clinical AI tools, each with a latent safety state (safe or unsafe) and observed evidence scores across five governance domains (Safety, Equity, Documentation, Accountability, Monitoring).

### Key Mechanism: Heterogeneous Evidence Profiles

Unsafe tools exhibit **heterogeneous** evidence profiles: scoring strongly in audit-visible domains (Safety, Documentation) and poorly in latent domains (Equity, Monitoring). This creates compensation opportunities for composite scoring methods while non-compensatory gates catch the latent-domain failures.

The heterogeneous profile is implemented via gate-specific Beta distribution shifts applied to unsafe tools (see `unsafe_gate_profile` in `params_default.json`).

### Three Decision Rules

1. **Non-compensatory gates**: Deploy only if ALL five gates pass their risk-tiered thresholds. Missing evidence treated as failure.
2. **Weighted composite**: Deploy if weighted average score exceeds a threshold. Two variants: matched (same deployment rate as gates) and moderate (~2.2× gate rate).
3. **Permissive baseline**: Deploy if at least 3 of 5 gates pass (majority rule).

### Override Pathway

Gates include a structured override: probability 0.10, maximum 1 failed gate, Safety and Monitoring gates excluded from override eligibility.

## Verification Simulations

Three scope conditions test where the gate advantage diminishes:
- **Uniform failure**: No heterogeneity; gate advantage eliminated
- **Random failure**: Partial heterogeneity; small gate leakage (0.9%)
- **Partial heterogeneity**: Latent-only failures; moderate gate leakage (0.8%)

## Sensitivity Analyses

- **Threshold sensitivity**: Multiplier range 0.60–1.40 applied to all thresholds
- **Noise robustness**: Observation noise SD swept from 0.01 to 0.20
- **Portfolio composition**: High-risk proportion 10%–50%
- **Unsafe probability**: ±30% of default values
