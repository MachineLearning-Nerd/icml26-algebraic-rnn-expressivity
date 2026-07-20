"""Run the dependency-free audit tests and write a durable gate input."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    payload = {"tests_passed": result.returncode == 0, "returncode": result.returncode,
               "stdout": result.stdout, "stderr": result.stderr}
    (ROOT / "outputs/test_results.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    if result.returncode:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
