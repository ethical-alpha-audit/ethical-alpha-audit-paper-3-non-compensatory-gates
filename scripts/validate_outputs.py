"""Validate output hashes against expected values.

Supports dual hash policy:
  - strict: hash mismatch is a FAIL
  - advisory: hash mismatch is a WARNING (logged but not fatal)

Requires only Python stdlib — suitable for reviewer quick validation.
"""

import json
import hashlib
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate():
    expected = load_json(BASE_DIR / "config" / "expected_outputs.json")
    failures = []
    warnings = []

    for item in expected["files"]:
        path = item["path"]
        required = item.get("required", True)
        expected_hash = item.get("sha256", "")
        hash_mode = item.get("hash_mode", "strict")
        file_path = BASE_DIR / path

        if not file_path.exists():
            if required:
                failures.append(f"Missing required output: {path}")
            continue

        if expected_hash:
            actual_hash = sha256_file(file_path)
            if actual_hash != expected_hash:
                msg = f"Hash mismatch for {path}: expected {expected_hash[:16]}..., got {actual_hash[:16]}..."
                if hash_mode == "advisory":
                    warnings.append(msg)
                else:
                    failures.append(msg)

    return failures, warnings


if __name__ == "__main__":
    failures, warnings = validate()

    if warnings:
        print(f"ADVISORY WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  WARN: {w}")
        print()

    if failures:
        print("VALIDATION FAILED")
        for failure in failures:
            print(f"  FAIL: {failure}")
        sys.exit(1)

    print("VALIDATION PASSED")
