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
