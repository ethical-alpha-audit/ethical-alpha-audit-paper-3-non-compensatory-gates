"""Single-command reproducibility orchestrator for Paper 2.

Usage:
    python reproduce_all.py          # full pipeline
    python reproduce_all.py --skip-notebooks  # hash + validate only
"""

import json
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def run_step(label, cmd):
    print(f"=== {label} ===")
    result = subprocess.run(cmd, cwd=BASE_DIR, text=True)
    if result.returncode != 0:
        print(f"FAIL: {label}")
        sys.exit(result.returncode)
    print(f"OK: {label}")


def main():
    settings = json.loads(
        (BASE_DIR / "config" / "harness_settings.json").read_text(encoding="utf-8")
    )
    os.environ["PYTHONHASHSEED"] = str(settings["python_hash_seed"])

    skip_notebooks = "--skip-notebooks" in sys.argv

    if not skip_notebooks:
        # Try notebook execution first; fall back to direct script execution
        try:
            import nbclient  # noqa: F401
            run_step("Notebook execution",
                     [sys.executable, "scripts/notebook_runner.py"])
        except ImportError:
            print("NOTE: nbclient not available — using direct engine execution")
            run_step("Direct engine execution",
                     [sys.executable, "scripts/run_direct.py"])

    run_step("Manifest generation",
             [sys.executable, "scripts/hash_manifest.py"])
    run_step("Output validation",
             [sys.executable, "scripts/validate_outputs.py"])

    # HTML export is optional (requires nbconvert)
    try:
        import nbconvert  # noqa: F401
        run_step("HTML export",
                 [sys.executable, "scripts/export_html.py"])
    except ImportError:
        print("NOTE: nbconvert not available — skipping HTML export")

    print("ALL STEPS PASSED")


if __name__ == "__main__":
    main()
