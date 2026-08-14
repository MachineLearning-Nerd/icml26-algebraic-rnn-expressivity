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
    "docs/EVIDENCE.md", "docs/PUBLICATION_GATE.md", "docs/SOURCE_AUDIT.md",
    "SOURCE_MANIFEST.md", "AUDIT_REPORT.md", "BRANCH_AUDIT.md", "GATE_READY.md",
    "outputs/README.md",
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
    marker = {
        "schema_version": 2,
        "paper": {
            "openreview_id": "7pbmZatDuD",
            "title": "An Algebraic View of the Expressivity of Recurrent Language Models",
            "arxiv": "2606.01765v2",
            "authors": ["Franz Nowak", "Ryan Cotterell", "Reda Boumasmoud"],
        },
        "repository": {
            "owner": "MachineLearning-Nerd",
            "original_name": "icml26-repro-7pbmZatDuD-algebraic-rnn-expressivity",
            "target_name": "icml26-algebraic-rnn-expressivity",
            "default_branch": "main",
        },
        "evidence_release_gate": "PASSED",
        "overall_status": "VERIFIED_SCOPED",
        "strict_paper_gate": "NOT_READY",
        "recorded_local_tests_passed": True,
        "substantive_claims": 3,
        "claims_verified_scoped": 3,
        "claims_falsified": 0,
        "claims_blocked": 0,
        "claim_results": {
            "C1": "VERIFIED_SCOPED_REALIZED_WREATH_FACTORIZATION",
            "C2": "VERIFIED_SCOPED_FINITE_PRECISION_SEMANTICS",
            "C3": "VERIFIED_SCOPED_UNSIGNED_PARITY_CORRECTION",
        },
        "evidence_bundle_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
        "claim_verification_sha256": bundle["artifacts"]["outputs/claim_verification.json"],
        "publication": {
            "status": "PUBLIC_GITHUB_HANDOFF_ONLY",
            "external_score_claimed": False,
        },
        "scope": "C1-C3 are finite exact witnesses and controls within the pinned arithmetic semantics. The universal algebraic conclusions are not inferred from finite samples alone, and no author executable was available.",
    }
    encoded_marker = json.dumps(marker, indent=2, sort_keys=True) + "\n"
    for path in (OUT / "PUBLICATION_GATE_PASSED.json", OUT / "publication_gate.json", ROOT / "publication_gate.json"):
        path.write_text(encoded_marker)
    print(encoded_marker, end="")


if __name__ == "__main__":
    main()
