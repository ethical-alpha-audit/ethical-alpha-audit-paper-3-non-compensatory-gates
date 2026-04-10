# Release Notes v1.0.0

Initial release of the Paper 2 reproducibility repository.

## Reproduces
- Primary heterogeneous model: 28.5% gate deployment, 0.0% unsafe deployment
- Composite (moderate): 62.7% deployment, 0.9% unsafe, 1.4% contamination
- Permissive baseline: 76.0% deployment, 2.2% unsafe
- 3 verification simulations (uniform, random, partial heterogeneity)
- Threshold sensitivity across 60%–140% multiplier range
- Noise robustness across SD 0.01–0.20
- Epic Sepsis Model case scenario (all 5 gates failed)
- Portfolio composition sensitivity (5 conditions)
- Unsafe probability sensitivity (5 conditions)
- 2 manuscript tables, 10 simulation figures, 1 static schematic
- Bootstrap 95% confidence intervals (n=1000) for all methods

## Annotations
- A-01: Permissive at noise SD=0.01 computes 2.0% vs manuscript 1.9%
- A-02: Threshold multipliers 0.60–0.65 show 0.1–0.2% gate leakage
