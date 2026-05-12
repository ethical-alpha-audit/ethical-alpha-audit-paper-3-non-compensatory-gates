"""Verify all required harness files exist."""

import json
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


def test_script_outputs_are_registered_for_validation_and_traceability():
    base = Path(__file__).resolve().parents[1]
    plan = json.loads((base / "config" / "notebook_plan.json").read_text(encoding="utf-8"))
    expected = json.loads((base / "config" / "expected_outputs.json").read_text(encoding="utf-8"))
    trace_map = json.loads((base / "config" / "trace_map.json").read_text(encoding="utf-8"))

    expected_paths = {item["path"] for item in expected["files"]}
    for step in plan.get("script_execution_order", []):
        for output_path in step["expected_outputs"]:
            assert output_path in expected_paths, f"Missing expected-output registration: {output_path}"
            assert output_path in trace_map, f"Missing trace-map registration: {output_path}"
