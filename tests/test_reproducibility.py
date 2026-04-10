"""Pre-execution checks: verify all engine, config, and notebook files exist."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_engine_exists():
    assert (ROOT / "src" / "run_simulation.py").exists()
    assert (ROOT / "src" / "run_verification.py").exists()
    assert (ROOT / "src" / "run_calibration_sensitivity.py").exists()
    assert (ROOT / "src" / "report_supplementary.py").exists()
    assert (ROOT / "src" / "params_default.json").exists()
    assert (ROOT / "src" / "__init__.py").exists()


def test_config_exists():
    assert (ROOT / "config" / "harness_settings.json").exists()
    assert (ROOT / "config" / "notebook_plan.json").exists()
    assert (ROOT / "config" / "expected_outputs.json").exists()
    assert (ROOT / "config" / "trace_map.json").exists()
    assert (ROOT / "config" / "presentation_config.json").exists()


def test_notebooks_exist():
    for nb in ["01_primary_simulation", "02_sensitivity_and_noise",
               "03_verification_simulations", "04_calibration_sensitivity",
               "05_tables_and_summary"]:
        assert (ROOT / "notebooks" / f"{nb}.ipynb").exists(), f"Missing {nb}.ipynb"


def test_static_data_exists():
    assert (ROOT / "data" / "static" / "Figure1_DecisionRuleComparison.png").exists()


def test_metadata_exists():
    for f in ["README.md", "CITATION.cff", ".zenodo.json", "LICENSE",
              "VERSION", "requirements.txt", "runtime.txt",
              "environment.yml", "environment.lock", "repro_manifest.json"]:
        assert (ROOT / f).exists(), f"Missing {f}"
