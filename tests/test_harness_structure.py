"""Verify all required harness files exist."""

from pathlib import Path


def test_harness_core_files_exist():
    base = Path(__file__).resolve().parents[1]
    required = [
        base / "reproduce_all.py",
        base / "config" / "notebook_plan.json",
        base / "config" / "expected_outputs.json",
        base / "config" / "harness_settings.json",
        base / "config" / "trace_map.json",
        base / "config" / "presentation_config.json",
        base / "scripts" / "notebook_runner.py",
        base / "scripts" / "hash_manifest.py",
        base / "scripts" / "validate_outputs.py",
        base / "scripts" / "export_html.py",
        base / "scripts" / "run_direct.py",
    ]
    for path in required:
        assert path.exists(), f"Missing required file: {path}"


def test_moderate_composite_cap_consistent():
    base = Path(__file__).resolve().parents[1]
    for relative in [
        "scripts/run_calibration_grid_2d.py",
        "scripts/run_counterhypothesis.py",
        "scripts/ch2_crossover_ci.py",
    ]:
        source = (base / relative).read_text(encoding="utf-8")
        assert "MODERATE_DEPLOYMENT_CAP = 0.85" in source
        assert "min(0.99" not in source
