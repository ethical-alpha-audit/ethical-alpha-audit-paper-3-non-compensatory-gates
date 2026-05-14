"""Regression checks for composite-moderate threshold calibration."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_helper_scripts_use_canonical_moderate_cap():
    """Helper scripts must match the primary engine's 0.85 deployment-rate cap."""
    helper_paths = [
        ROOT / "scripts" / "ch2_crossover_ci.py",
        ROOT / "scripts" / "run_calibration_grid_2d.py",
        ROOT / "scripts" / "run_counterhypothesis.py",
    ]

    for path in helper_paths:
        source = path.read_text(encoding="utf-8")
        assert "min(0.99" not in source
        assert "0.85" in source
