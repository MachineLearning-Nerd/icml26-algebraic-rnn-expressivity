# Claim 2 — Proposition 3.20 exact cascade certificate

## Source and scope

- Paper: *An Algebraic View of Expressivity of Recurrent Language Models* (`arXiv:2606.01765`).
- Primary HTML: `https://ar5iv.labs.arxiv.org/html/2606.01765`.
- HTML SHA-256: `e6b55eaf773981b45e793342d31dcae1c4c3a68d3aa1b54754b8cc672d1590bd`.
- Scope: Proposition 3.20 and Appendix F, using Definitions 2.4, 3.5, 3.9, and 3.11, Remark 2.10, and Lemma 3.12.

Proposition 3.20 states, up to the canonical wreath-product isomorphism,

```text
W_(R rhd_tau R')^T = W_R^T wr W_R'^T
M_R^T divides M_(R rhd_tau R')^T <= W_R^T wr W_R'^T.
```

## What was checked

`repro/src/verify_prop_3_20_exact.py` records the complete Appendix-F dependency chain:

1. cascade juxtaposition concatenates the `N` and `N'` layer sequences;
2. Definition 3.11 expands the ambient realized wreath product over all `N+N'` factors;
3. Remark 2.10 canonically reassociates those factors into the two component wreath products;
4. Lemma 3.12 embeds the cascade's realized transition monoid in that ambient product;
5. strict feedforward wiring makes the first `N` coordinates independent of later coordinates;
6. the first-coordinate projection therefore induces a surjective monoid morphism onto `M_R^T`, proving division.

The universal conclusion is supported by that paper-exact proof chain under its hypotheses. Exact finite transformation-monoid cases only corroborate the projection algebra; they are not used to infer the theorem from samples.

## Deterministic results

```text
proof_chain_valid: true
canonical regroup checks: 144/144
projection quotient witnesses: 12/12
projection independence: true
projection surjectivity: true
projection homomorphism: true
RESULT_SHA256=b374b5ec284e02c5190e3d0feb1a4c93dda8505ef27aae6d7f7f8a613edc2ebf
```

The independent no-import auditor uses different cascade generators and validates 15 additional projection quotients.

```text
independent_chain_valid: true
independent_projection_cases: 15/15
audit_passed: true
```

## Fail-sensitive controls

The primary verifier rejects a proof missing canonical reassociation, factorization, or the feedforward projection, and rejects a conclusion placed before its dependencies. It also detects a corrupted cascade where a later coordinate feeds back into the first coordinates. The independent auditor separately rejects a duplicate step, a missing division step, and a forward dependency.

## Reproduction

```bash
python repro/src/verify_prop_3_20_exact.py
python repro/src/audit_prop_3_20_exact.py
```

Artifact hashes:

```text
verify_prop_3_20_exact.py  534227d4a691b942acd05cd1fb403c697908cd93be06a7021740c299ac75e9ba
audit_prop_3_20_exact.py   63815d62fea0c696482dde636c98c80a1748cb0ffbc10078de3b8eab4e1d5c8b
```

This page strengthens official Claim 2 only. It does not alter or weaken the evidence for the other three judged claims.
