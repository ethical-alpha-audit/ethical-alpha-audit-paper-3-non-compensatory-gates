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


def test_notebook_runner_uses_notebook_kernelspec():
    base = Path(__file__).resolve().parents[1]
    runner_source = (base / "scripts" / "notebook_runner.py").read_text(encoding="utf-8")

    assert "kernel_name=" not in runner_source

    plan = json.loads((base / "config" / "notebook_plan.json").read_text(encoding="utf-8"))
    for item in plan["execution_order"]:
        notebook = json.loads((base / item["path"]).read_text(encoding="utf-8"))
        assert notebook["metadata"]["kernelspec"]["name"] == "python3"
