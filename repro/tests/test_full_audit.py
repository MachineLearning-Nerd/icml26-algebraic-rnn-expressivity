import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class FullAuditTest(unittest.TestCase):
    def test_complete_audit_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "audit.json"
            result = subprocess.run(
                [sys.executable, "repro/src/full_audit.py", "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=True,
            )
            report = json.loads(output.read_text())
        self.assertIn("sha256=", result.stdout)
        self.assertTrue(report["outcome"].startswith("3/3"))
        self.assertTrue(all(report["claims"][claim]["result"] == "verified"
                            for claim in ("C1", "C2", "C3")))
        self.assertTrue(report["claims"]["C1"]["ambient_reset_rejected_as_unrealized"])
        self.assertTrue(report["claims"]["C2"]["signed_multiplier_control_rejected"])
        self.assertTrue(report["claims"]["C3"]["contains_C2"])
