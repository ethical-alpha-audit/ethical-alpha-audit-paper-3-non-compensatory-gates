"""Regression checks for the composite-moderate deployment policy."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_new_analysis_scripts_use_established_moderate_cap():
    """New Stage 5 analyses should match the primary engine's 85% cap."""
    script_paths = [
        ROOT / "scripts" / "run_counterhypothesis.py",
        ROOT / "scripts" / "run_calibration_grid_2d.py",
        ROOT / "scripts" / "ch2_crossover_ci.py",
    ]

    for path in script_paths:
        source = path.read_text(encoding="utf-8")
        assert "min(0.99" not in source
        assert "0.85" in source, f"Missing established moderate cap in {path}"


def test_ch3_artifact_reflects_moderate_cap():
    output_path = ROOT / "outputs" / "counter_hypothesis" / "ch3_uniform_high_quality.json"
    with output_path.open(encoding="utf-8") as f:
        ch3 = json.load(f)

    moderate = ch3["results"]["Composite (moderate)"]
    assert moderate["deployment_rate"] == 0.85
    assert moderate["unsafe_deployment_rate"] == 0.123
