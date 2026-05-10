"""Regression checks for derived-analysis composite threshold calibration."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_recent_analysis_scripts_use_engine_moderate_cap():
    """The moderate composite target must stay capped like the core engine."""
    scripts = [
        ROOT / "scripts" / "run_counterhypothesis.py",
        ROOT / "scripts" / "run_calibration_grid_2d.py",
        ROOT / "scripts" / "ch2_crossover_ci.py",
    ]

    for script in scripts:
        source = script.read_text(encoding="utf-8")
        assert "COMPOSITE_MODERATE_MAX_DEPLOY_RATE = 0.85" in source
        assert "min(0.99" not in source
