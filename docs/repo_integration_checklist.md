# Pre-Submission Checklist

1. [ ] `python -m pytest tests/ -v` — all structural tests pass
2. [ ] `python reproduce_all.py` — ALL STEPS PASSED
3. [ ] Second clean run produces identical STRICT hashes
4. [ ] README reviewer quick-start works
5. [ ] `docs/html/` contains 5 HTML files (if nbconvert available)
6. [ ] CITATION.cff DOI field populated
7. [ ] .zenodo.json metadata complete
8. [ ] VERSION matches across all files
9. [ ] Git tag v1.0.0 applied
10. [ ] Zenodo DOI reserved and backfilled into manuscript
11. [ ] Engine file hashes match docs/provenance.md
12. [ ] `python scripts/validate_outputs.py` returns VALIDATION PASSED
