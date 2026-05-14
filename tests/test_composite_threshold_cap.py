"""Regression checks for the canonical composite-moderate deployment cap."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_counter_hypothesis_uses_canonical_moderate_cap():
    source = (ROOT / "scripts" / "run_counterhypothesis.py").read_text(encoding="utf-8")

    assert "min(gate_rate * 2.2, 0.85)" in source
    assert "min(0.99, gate_rate * 2.2)" not in source


def test_calibration_grid_uses_canonical_moderate_cap():
    source = (ROOT / "scripts" / "run_calibration_grid_2d.py").read_text(encoding="utf-8")

    assert "min(gate_rate * 2.2, 0.85)" in source
    assert "min(0.99, gate_rate * 2.2)" not in source


def test_ch2_crossover_uses_canonical_moderate_cap():
    source = (ROOT / "scripts" / "ch2_crossover_ci.py").read_text(encoding="utf-8")

    assert "min(gate_rate * 2.2, 0.85)" in source
    assert "min(0.99, gate_rate * 2.2)" not in source

