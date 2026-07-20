# Claim 3


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_024174461924", "created_at": "2026-07-20T10:22:08+00:00", "title": "Unsigned parity correction"}
-->
Replays the source 4-bit unsigned-wraparound parity recurrence for every binary word through length 10. It is a C2 construction, not a mod-3 result.


---
<!-- trackio-cell
{"type": "code", "id": "cell_de6610e68035", "created_at": "2026-07-20T10:22:08+00:00", "title": "Tests and exact parity control", "command": [".venv/bin/python", "repro/src/run_tests.py"], "exit_code": 0, "duration_s": 0.302}
-->
````bash
$ .venv/bin/python repro/src/run_tests.py
````

exit 0 · 0.3s


````python title=run_tests.py
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

````


````output
test_complete_audit_is_reproducible (test_full_audit.FullAuditTest.test_complete_audit_is_reproducible) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.208s

OK

````
