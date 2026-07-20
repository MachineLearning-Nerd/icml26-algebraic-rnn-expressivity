"""Hash-address the complete local evidence set after passing the full gate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"
REQUIRED = tuple(ROOT / path for path in (
    "README.md", "STATUS.md", "docs/source_pins.json", "docs/live_claims_2026-07-20.json",
    "docs/arxiv_source.tar", "docs/primary.pdf", "docs/source/main.tex",
    ".trackio/metadata.json", ".trackio/logbook/logbook.json",
    "repro/src/full_audit.py", "repro/src/run_tests.py", "repro/src/verify_claims.py",
    "repro/src/build_evidence_bundle.py", "repro/tests/test_full_audit.py", "outputs/audit.json",
    "outputs/test_results.json", "outputs/claim_verification.json"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    verification = json.loads((OUT / "claim_verification.json").read_text())
    if not (verification["all_claims_complete"] and verification["tests_passed"]
            and verification["earned_points"] == 6 and verification["publication_gate_passed"]):
        raise SystemExit("cannot bundle an incomplete reproduction")
    bundle = {"paper": "7pbmZatDuD", "gate": "FULL_GATE_READY", "live_claim_count": 3,
              "earned_points": 6,
              "claim_outcomes": {"C1": "verified_realized_wreath_factorization",
                                 "C2": "verified_fixed_semantics_aperiodicity_controls",
                                 "C3": "verified_unsigned_parity_correction"},
              "artifacts": {str(p.relative_to(ROOT)): sha256(p) for p in REQUIRED}}
    encoded = json.dumps(bundle, indent=2, sort_keys=True) + "\n"
    (OUT / "evidence_bundle.json").write_text(encoded)
    marker = {"gate": "FULL_GATE_READY", "queue_marker": "FULL_GATE_READY: 7pbmZatDuD",
              "paper": "7pbmZatDuD", "evidence_bundle_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
              "claim_verification_sha256": bundle["artifacts"]["outputs/claim_verification.json"],
              "claims_complete": True, "earned_points": 6, "tests_passed": True,
              "publication_gate_passed": True}
    (OUT / "PUBLICATION_GATE_PASSED.json").write_text(json.dumps(marker, indent=2) + "\n")
    print(json.dumps(marker, indent=2))


if __name__ == "__main__":
    main()
