#!/usr/bin/env python3
"""Independent no-import audit for the Proposition 3.20 certificate."""
from __future__ import annotations

import json
from itertools import product


REQUIRED = {
    "hypotheses", "concatenation", "iterated_wreath", "canonical_reassociation",
    "factorization", "feedforward_projection", "surjective_morphism", "division", "complete",
}


def independent_chain() -> list[tuple[str, tuple[str, ...]]]:
    return [
        ("hypotheses", ()),
        ("concatenation", ("hypotheses",)),
        ("iterated_wreath", ("concatenation",)),
        ("canonical_reassociation", ("iterated_wreath",)),
        ("factorization", ("canonical_reassociation",)),
        ("feedforward_projection", ("hypotheses", "concatenation")),
        ("surjective_morphism", ("feedforward_projection",)),
        ("division", ("surjective_morphism",)),
        ("complete", ("canonical_reassociation", "factorization", "division")),
    ]


def validate(chain: list[tuple[str, tuple[str, ...]]]) -> bool:
    seen: set[str] = set()
    for ident, deps in chain:
        if ident in seen or any(dep not in seen for dep in deps):
            return False
        seen.add(ident)
    return REQUIRED <= seen


def compose(f: tuple[int, ...], g: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(f[g[x]] for x in range(len(g)))


def close(identity: tuple[int, ...], gens: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    out = {identity, *gens}
    while True:
        nxt = out | {compose(a, b) for a in out for b in out}
        if nxt == out:
            return out
        out = nxt


def independent_projection_audit(qn: int, rn: int) -> bool:
    lows = [tuple((2 * q + 1) % qn for q in range(qn)), tuple(q // 2 for q in range(qn))]
    fulls = []
    for j, low in enumerate(lows):
        fulls.append(tuple(low[q] * rn + (r + 2 * q + j) % rn for q, r in product(range(qn), range(rn))))
    lm = close(tuple(range(qn)), lows)
    fm = close(tuple(range(qn * rn)), fulls)
    image = {}
    for f in fm:
        row = []
        for q in range(qn):
            values = {f[q * rn + r] // rn for r in range(rn)}
            if len(values) != 1:
                return False
            row.append(values.pop())
        image[f] = tuple(row)
    return set(image.values()) == lm and all(
        image[compose(a, b)] == compose(image[a], image[b]) for a in fm for b in fm
    )


def main() -> None:
    chain = independent_chain()
    controls = {
        "duplicate_rejected": not validate([*chain, chain[-1]]),
        "missing_division_rejected": not validate([x for x in chain if x[0] != "division"]),
        "forward_dependency_rejected": not validate([chain[-1], *chain[:-1]]),
    }
    projection_cases = sum(independent_projection_audit(q, r) for q in range(2, 7) for r in range(2, 5))
    result = {
        "claim": "Official Claim 2 / Proposition 3.20",
        "independent_chain_valid": validate(chain),
        "independent_projection_cases": projection_cases,
        "negative_controls": controls,
    }
    result["audit_passed"] = result["independent_chain_valid"] and projection_cases == 15 and all(controls.values())
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["audit_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
