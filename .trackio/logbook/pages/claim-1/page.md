# Claim 1


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_1ab05370a7b3", "created_at": "2026-07-20T10:22:04+00:00", "title": "Realized wreath factorization"}
-->
Exact two-layer left-wreath witness. Negative control: a reset available only in the ambient monoid is rejected as unrealized.


---
<!-- trackio-cell
{"type": "code", "id": "cell_b4412789ab78", "created_at": "2026-07-20T10:22:05+00:00", "title": "Exact C1 audit", "command": [".venv/bin/python", "repro/src/full_audit.py", "--output", "outputs/audit.json"], "exit_code": 0, "duration_s": 0.204}
-->
````bash
$ .venv/bin/python repro/src/full_audit.py --output outputs/audit.json
````

exit 0 · 0.2s


````python title=full_audit.py
#!/usr/bin/env python3
"""Exact, dependency-free audit of the three live claims for 7pbmZatDuD.

All transformations are represented extensionally over finite state sets.  This
avoids relying on an algebra package or on the paper's unavailable executable.
The checks deliberately retain the source's conditions: realized (not merely
ambient) wreath dynamics, a fixed arithmetic evaluation order, nonnegative
multipliers for the aperiodicity result, and unsigned *wraparound* arithmetic
for the constructive parity counter.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import struct
from pathlib import Path
from typing import Callable, Iterable


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/source/main.tex"


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """left after right, the convention used for transformation monoids."""
    return tuple(left[right[x]] for x in range(len(right)))


def identity(n: int) -> tuple[int, ...]:
    return tuple(range(n))


def generated(generators: Iterable[tuple[int, ...]]) -> set[tuple[int, ...]]:
    generators = tuple(generators)
    assert generators and len({len(g) for g in generators}) == 1
    known = {identity(len(generators[0]))}
    frontier = list(generators)
    while frontier:
        item = frontier.pop()
        if item in known:
            continue
        known.add(item)
        for other in tuple(known):
            frontier.extend((compose(item, other), compose(other, item)))
    return known


def power(f: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = identity(len(f))
    for _ in range(exponent):
        result = compose(f, result)
    return result


def aperiodicity_witness(monoid: Iterable[tuple[int, ...]]) -> tuple[bool, int | None]:
    elements = tuple(monoid)
    # A finite transformation monoid needs no exponent beyond its cardinality
    # to find the eventual idempotent tail when it is aperiodic.
    for exponent in range(1, len(elements) + 1):
        if all(power(m, exponent) == power(m, exponent + 1) for m in elements):
            return True, exponent
    return False, None


def monotone(f: tuple[int, ...]) -> bool:
    return all(f[i] <= f[i + 1] for i in range(len(f) - 1))


def f32(x: float) -> float:
    return struct.unpack(">f", struct.pack(">f", x))[0]


def source_audit() -> dict:
    text = SOURCE.read_text(encoding="utf-8")
    required = {
        "wreath definition": "(left) wreath product",
        "realized/ambient distinction": "realized wreath product",
        "recurrence consistency": "Recurrence-consistent evaluation",
        "floating nonnegative theorem": "Nonnegative floating-point updates are aperiodic",
        "parity impossibility": "no nonnegative diagonal SSM over",
        "unsigned construction": "Parity over unsigned integers",
        "prior-claim correction": "unstated assumption that the arithmetic is floating point",
    }
    absent = [label for label, needle in required.items() if needle not in text]
    if absent:
        raise AssertionError(f"source anchor(s) absent: {absent}")
    executables = [p.name for p in (ROOT / "docs/source").rglob("*")
                   if p.suffix in {".py", ".ipynb", ".sh"}]
    if executables:
        raise AssertionError(f"unexpected author executables: {executables}")
    return {"anchors": list(required), "author_executables": executables}


def claim_1_wreath_factorization() -> dict:
    # Lower layer: input 0 is identity and input 1 toggles the lower bit.
    # Upper layer sees the old lower bit and toggles iff that bit is 1, matching
    # the source's stated left-wreath convention.
    # This is an explicit two-layer recurrence on S1 x S2, factored as a left
    # wreath action (M1,S1) wr (M2,S2).
    states = tuple(itertools.product(range(2), repeat=2))
    index = {s: i for i, s in enumerate(states)}
    global_maps: list[tuple[int, ...]] = []
    for token in (0, 1):
        global_maps.append(tuple(index[(s1 ^ token, s2 ^ s1)]
                                 for s1, s2 in states))
    lower_id, lower_toggle = (0, 1), (1, 0)
    upper_id, upper_toggle = (0, 1), (1, 0)
    lower_maps = (lower_id, lower_toggle)
    upper_maps = (upper_id, upper_toggle)
    def wreath_action(lower: tuple[int, ...], phi: tuple[tuple[int, ...], tuple[int, ...]]):
        return tuple(index[(lower[s1], phi[s1][s2])] for s1, s2 in states)
    factor_pairs = [
        (lower_maps[token], tuple(upper_maps[s1] for s1 in range(2)))
        for token in (0, 1)
    ]
    factored = [wreath_action(*pair) for pair in factor_pairs]
    assert factored == global_maps
    realized = generated(global_maps)
    # Negative control: make the ambient lower monoid include reset-to-zero,
    # but restrict the input alphabet to {0,1}; realized transitions must not
    # silently acquire that ambient reset transformation.
    reset_lower = (0, 0)
    ambient_lower = generated((lower_id, lower_toggle, reset_lower))
    ambient_witness = wreath_action(reset_lower, (upper_id, upper_id))
    assert ambient_witness not in realized
    return {
        "result": "verified",
        "state_count": len(states),
        "realized_transition_monoid_size": len(realized),
        "factorization_exact_for_each_token": True,
        "ambient_lower_monoid_size": len(ambient_lower),
        "ambient_reset_rejected_as_unrealized": True,
        "scope": "finite two-layer deterministic recurrence; a witness for the source framework, not a survey claim about all RNNs",
    }


def chain_affine(domain: tuple[int, ...], multiplier: int, bias: int) -> tuple[int, ...]:
    lo, hi = domain[0], domain[-1]
    return tuple(min(hi, max(lo, multiplier * x + bias)) - lo for x in domain)


def claim_2_finite_precision() -> dict:
    # Ordered finite-chain surrogates test the proof mechanism directly: all
    # nonnegative affine saturated updates are order preserving and their
    # generated monoids become idempotent.  The source supplies the full IEEE
    # theorem; this clean-room audit does not claim that this small chain is IEEE.
    cases = []
    for width in (3, 5, 7):
        domain = tuple(range(-(width // 2), width // 2 + 1))
        updates = [chain_affine(domain, a, b)
                   for a in (0, 1, 2) for b in (-1, 0, 1)]
        assert all(monotone(f) for f in updates)
        monoid = generated(updates)
        ap, exponent = aperiodicity_witness(monoid)
        assert ap
        cases.append({"domain": list(domain), "monoid_size": len(monoid),
                      "aperiodicity_exponent": exponent})
    # Signed multiplier is a decisive control: negation has a 2-cycle, so the
    # nonnegative condition cannot be dropped.
    signed_domain = (-1, 0, 1)
    negate = tuple((-x) - signed_domain[0] for x in signed_domain)
    signed_monoid = generated((negate,))
    signed_ap, _ = aperiodicity_witness(signed_monoid)
    assert not signed_ap and power(negate, 2) == identity(3) and negate != identity(3)
    # Float32 gives the paper's concrete reason a fixed evaluation order is part
    # of the semantics rather than a presentation choice.
    a, b, c = f32(1.0), f32(2.0 ** 24), f32(-(2.0 ** 24))
    left = f32(f32(a + b) + c)
    right = f32(a + f32(b + c))
    assert (left, right) == (0.0, 1.0)
    return {
        "result": "verified",
        "finite_ordered_models": cases,
        "all_nonnegative_updates_monotone": True,
        "all_enumerated_nonnegative_monoids_aperiodic": True,
        "signed_multiplier_control_rejected": True,
        "float32_associativity_control": {"(a+b)+c": left, "a+(b+c)": right,
                                           "fixed_evaluation_order_required": left != right},
        "scope": "finite deterministic semantics with NaNs excluded and a fixed recurrence-consistent order",
    }


def claim_3_semantics_correction() -> dict:
    # Source Example: p=4, A=1, B(0)=0, B(1)=8, initial=15, accept={15}.
    modulus, initial, accept = 16, 15, {15}
    transitions = {
        0: tuple(range(modulus)),
        1: tuple((s + 8) % modulus for s in range(modulus)),
    }
    words_checked = 0
    for length in range(11):
        for word in itertools.product((0, 1), repeat=length):
            state = initial
            for symbol in word:
                state = transitions[symbol][state]
            assert (state in accept) == (sum(word) % 2 == 0)
            words_checked += 1
    parity_monoid = generated(transitions.values())
    parity_ap, _ = aperiodicity_witness(parity_monoid)
    add_eight = transitions[1]
    assert len(parity_monoid) == 2 and not parity_ap
    assert power(add_eight, 2) == identity(modulus) and add_eight != identity(modulus)
    # A C3 control records the source's boundary: this 4-bit construction is a
    # C2 parity construction, not evidence for arbitrary moduli.
    add_one = tuple((s + 1) % modulus for s in range(modulus))
    assert power(add_one, 16) == identity(modulus)
    assert all(power(add_one, k) != identity(modulus) for k in range(1, 16))
    return {
        "result": "verified",
        "unsigned_wraparound_bits": 4,
        "nonnegative_recurrence": {"A": 1, "B(0)": 0, "B(1)": 8},
        "parity_words_exhaustively_checked_through_length": 10,
        "word_count": words_checked,
        "transition_monoid_size": len(parity_monoid),
        "contains_C2": True,
        "floating_nonnegative_aperiodicity_conflicts_with_C2": True,
        "C3_boundary_control": "the explicit construction has order 2 only; no claim that it implements mod-3",
        "scope": "same nonnegative diagonal recurrence under 4-bit unsigned wraparound versus fixed floating-point semantics",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="outputs/audit.json")
    args = parser.parse_args()
    report = {
        "paper": "7pbmZatDuD",
        "title": "An Algebraic View of the Expressivity of Recurrent Language Models",
        "source_audit": source_audit(),
        "claims": {
            "C1": claim_1_wreath_factorization(),
            "C2": claim_2_finite_precision(),
            "C3": claim_3_semantics_correction(),
        },
        "outcome": "3/3 live claims independently reproduced within their stated scope",
    }
    serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    destination = ROOT / args.output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    print("sha256=" + hashlib.sha256(serialized.encode()).hexdigest())


if __name__ == "__main__":
    main()

````


````json title=audit.json
{
  "claims": {
    "C1": {
      "ambient_lower_monoid_size": 4,
      "ambient_reset_rejected_as_unrealized": true,
      "factorization_exact_for_each_token": true,
      "realized_transition_monoid_size": 8,
      "result": "verified",
      "scope": "finite two-layer deterministic recurrence; a witness for the source framework, not a survey claim about all RNNs",
      "state_count": 4
    },
    "C2": {
      "all_enumerated_nonnegative_monoids_aperiodic": true,
      "all_nonnegative_updates_monotone": true,
      "finite_ordered_models": [
        {
          "aperiodicity_exponent": 2,
          "domain": [
            -1,
            0,
            1
          ],
          "monoid_size": 10
        },
        {
          "aperiodicity_exponent": 4,
          "domain": [
            -2,
            -1,
            0,
            1,
            2
          ],
          "monoid_size": 82
        },
        {
          "aperiodicity_exponent": 6,
          "domain": [
            -3,
            -2,
            -1,
            0,
            1,
            2,
            3
          ],
          "monoid_size": 377
        }
      ],
      "float32_associativity_control": {
        "(a+b)+c": 0.0,
        "a+(b+c)": 1.0,
        "fixed_evaluation_order_required": true
      },
      "result": "verified",
      "scope": "finite deterministic semantics with NaNs excluded and a fixed recurrence-consistent order",
      "signed_multiplier_control_rejected": true
    },
    "C3": {
      "C3_boundary_control": "the explicit construction has order 2 only; no claim that it implements mod-3",
      "contains_C2": true,
      "floating_nonnegative_aperiodicity_conflicts_with_C2": true,
      "nonnegative_recurrence": {
        "A": 1,
        "B(0)": 0,
        "B(1)": 8
      },
      "parity_words_exhaustively_checked_through_length": 10,
      "result": "verified",
      "scope": "same nonnegative diagonal recurrence under 4-bit unsigned wraparound versus fixed floating-point semantics",
      "transition_monoid_size": 2,
      "unsigned_wraparound_bits": 4,
      "word_count": 2047
    }
  },
  "outcome": "3/3 live claims independently reproduced within their stated scope",
  "paper": "7pbmZatDuD",
  "source_audit": {
    "anchors": [
      "wreath definition",
      "realized/ambient distinction",
      "recurrence consistency",
      "floating nonnegative theorem",
      "parity impossibility",
      "unsigned construction",
      "prior-claim correction"
    ],
    "author_executables": []
  },
  "title": "An Algebraic View of the Expressivity of Recurrent Language Models"
}

````


````output
{
  "claims": {
    "C1": {
      "ambient_lower_monoid_size": 4,
      "ambient_reset_rejected_as_unrealized": true,
      "factorization_exact_for_each_token": true,
      "realized_transition_monoid_size": 8,
      "result": "verified",
      "scope": "finite two-layer deterministic recurrence; a witness for the source framework, not a survey claim about all RNNs",
      "state_count": 4
    },
    "C2": {
      "all_enumerated_nonnegative_monoids_aperiodic": true,
      "all_nonnegative_updates_monotone": true,
      "finite_ordered_models": [
        {
          "aperiodicity_exponent": 2,
          "domain": [
            -1,
            0,
            1
          ],
          "monoid_size": 10
        },
        {
          "aperiodicity_exponent": 4,
          "domain": [
            -2,
            -1,
            0,
            1,
            2
          ],
          "monoid_size": 82
        },
        {
          "aperiodicity_exponent": 6,
          "domain": [
            -3,
            -2,
            -1,
            0,
            1,
            2,
            3
          ],
          "monoid_size": 377
        }
      ],
      "float32_associativity_control": {
        "(a+b)+c": 0.0,
        "a+(b+c)": 1.0,
        "fixed_evaluation_order_required": true
      },
      "result": "verified",
      "scope": "finite deterministic semantics with NaNs excluded and a fixed recurrence-consistent order",
      "signed_multiplier_control_rejected": true
    },
    "C3": {
      "C3_boundary_control": "the explicit construction has order 2 only; no claim that it implements mod-3",
      "contains_C2": true,
      "floating_nonnegative_aperiodicity_conflicts_with_C2": true,
      "nonnegative_recurrence": {
        "A": 1,
        "B(0)": 0,
        "B(1)": 8
      },
      "parity_words_exhaustively_checked_through_length": 10,
      "result": "verified",
      "scope": "same nonnegative diagonal recurrence under 4-bit unsigned wraparound versus fixed floating-point semantics",
      "transition_monoid_size": 2,
      "unsigned_wraparound_bits": 4,
      "word_count": 2047
    }
  },
  "outcome": "3/3 live claims independently reproduced within their stated scope",
  "paper": "7pbmZatDuD",
  "source_audit": {
    "anchors": [
      "wreath definition",
      "realized/ambient distinction",
      "recurrence consistency",
      "floating nonnegative theorem",
      "parity impossibility",
      "unsigned construction",
      "prior-claim correction"
    ],
    "author_executables": []
  },
  "title": "An Algebraic View of the Expressivity of Recurrent Language Models"
}
sha256=fb330bd0590db28677b4acd8745239c3358f3ad9af1f333d2e54fd7da640ac9a

````
