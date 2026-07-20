# Algebraic RNN expressivity reproduction

Clean-room, source-pinned reproduction of *An Algebraic View of the
Expressivity of Recurrent Language Models* (ICML 2026; OpenReview
`7pbmZatDuD`; arXiv `2606.01765`).

The current challenge contract has three claims (six possible points):

1. Wreath-product transformation semigroups provide the unifying framework.
2. Fixed arithmetic semantics enable rigorous finite-precision analysis.
3. The framework corrects representative RNN/LSTM/SSM expressivity claims.

The source ships no executable author artifact. This package independently
enumerates finite transformation monoids and reconstructs the stated
floating-point versus unsigned-integer counter cases, retaining every relevant
architectural and arithmetic condition.

## Outcome

All three live claims are locally complete (6/6 points) within their stated
scope. The evidence is deliberately finite and exact: it does not substitute a
training proxy for an algebraic result.

- C1: an explicit two-layer recurrence factorizes through its *realized* left
  wreath action. A reset present only in the ambient lower monoid is rejected.
- C2: generated monoids from nonnegative saturated updates on three finite
  ordered domains are aperiodic; the signed-multiplier and Float32
  reassociation controls fail as they should.
- C3: the source's 4-bit unsigned-wraparound recurrence accepts parity for all
  2,047 binary words through length 10 and contains a nontrivial C2. This
  contrasts with the fixed-floating-point, nonnegative aperiodicity setting.

## Reproduce

```bash
uv venv --python 3.12 .venv
.venv/bin/python repro/src/full_audit.py --output outputs/audit.json
.venv/bin/python repro/src/run_tests.py
.venv/bin/python repro/src/verify_claims.py
.venv/bin/python repro/src/build_evidence_bundle.py
```

No GPU, HF Job, or external package is required for this exact audit.

## Scope and limits

The audit is a clean-room finite witness and control suite, not an independent
reproof of every general theorem in the paper. In particular, its ordered
finite-chain enumeration demonstrates the aperiodicity mechanism; it does not
claim that a small saturated integer chain is IEEE floating point. The claim
verifier preserves the source's NaN exclusion, fixed recurrence-consistent
evaluation order, nonnegative multiplier condition, and 4-bit *unsigned
wraparound* condition.

|  | This reproduction | Full replication |
| --- | --- | --- |
| Scope | Exact finite witnesses, all live claims, controls | General formal theorems over all source-defined finite formats/architectures |
| Hardware | Local CPU | Symbolic proof/verification infrastructure; no GPU requirement inherent |
| Time | Seconds | Research-proof effort |
| Cost | $0 | Not estimated |
| Outcome | 3/3 contract claims complete, evidence hash-addressed | Outside this clean-room audit's scope |
