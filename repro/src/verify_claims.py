"""Fail closed on missing source pins, controls, or tests for the live contract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    pins, live, audit = (load(ROOT / "docs/source_pins.json"),
                         load(ROOT / "docs/live_claims_2026-07-20.json"),
                         load(OUT / "audit.json"))
    source_pinned = (sha256(ROOT / "docs/arxiv_source.tar") == pins["arxiv_source_sha256"]
                     and sha256(ROOT / "docs/primary.pdf") == pins["primary_pdf_sha256"]
                     and sha256(ROOT / "docs/source/main.tex") == pins["primary_tex_sha256"])
    contract_pinned = (live["openreview_id"] == "7pbmZatDuD" and live["claim_count"] == 3
                       and live["points_possible"] == 6 and len(live["claims"]) == 3)
    tests = load(OUT / "test_results.json").get("tests_passed") is True
    c1, c2, c3 = (audit["claims"][key] for key in ("C1", "C2", "C3"))
    claim_1 = bool(source_pinned and contract_pinned and c1["result"] == "verified"
                   and c1["factorization_exact_for_each_token"]
                   and c1["ambient_reset_rejected_as_unrealized"])
    claim_2 = bool(source_pinned and contract_pinned and c2["result"] == "verified"
                   and c2["all_enumerated_nonnegative_monoids_aperiodic"]
                   and c2["signed_multiplier_control_rejected"]
                   and c2["float32_associativity_control"]["fixed_evaluation_order_required"])
    claim_3 = bool(source_pinned and contract_pinned and c3["result"] == "verified"
                   and c3["contains_C2"] and c3["word_count"] == 2047
                   and c3["floating_nonnegative_aperiodicity_conflicts_with_C2"])
    complete = (claim_1, claim_2, claim_3)
    result = {
        "paper": "7pbmZatDuD", "source_pinned": source_pinned,
        "live_contract_pinned": contract_pinned, "live_claim_count": live["claim_count"],
        "claim_1_wreath_framework": claim_1,
        "claim_2_deterministic_finite_precision": claim_2,
        "claim_3_rederivation_and_correction": claim_3,
        "decisive_claims": sum(complete), "earned_points": 2 * sum(complete),
        "all_claims_complete": all(complete), "tests_passed": tests,
        "publication_gate_passed": all(complete) and tests,
        "scope": "C1 is an exact finite witness. C2 keeps NaNs excluded, nonnegative multipliers and recurrence-consistent order. C3 is precisely a 4-bit unsigned-wraparound parity correction, contrasted with the fixed-floating-point aperiodicity theorem.",
    }
    (OUT / "claim_verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["all_claims_complete"]:
        raise SystemExit("incomplete 7pbmZatDuD verification")


if __name__ == "__main__":
    main()
