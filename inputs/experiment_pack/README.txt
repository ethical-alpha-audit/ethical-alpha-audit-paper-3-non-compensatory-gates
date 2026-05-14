Paper 3 Experiment Bundle: Gate Decomposition Comparison (A02)
==============================================================

Three alternative gate decompositions plus the five-gate baseline were
evaluated to test whether the non-compensatory safety advantage persists
across structural alternatives. A pre-specified seven-gate model (D4)
was excluded because the simulation does not generate the required
observable features.

Key Results:
  NC unsafe = 0.000 for all 4 decomposition configurations
  Comp(0.50) unsafe: D0=4.0%, D1=7.1%, D2=4.6%, D3=4.0%
  All comparisons exclude overrides for consistent cross-structure comparison

Reproduction:
  Requires Python 3.12+, numpy, pandas
  Requires P2 simulation framework (companion repository)
  Seed: 20260304 (portfolio), 42 (D3 noise)
