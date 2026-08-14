# ICML 2026 — An Algebraic View of Recurrent Language-Model Expressivity

This repository contains a clean-room, source-pinned audit of [*An Algebraic View of the Expressivity of Recurrent Language Models*](https://arxiv.org/abs/2606.01765) by Franz Nowak, Ryan Cotterell, and Reda Boumasmoud.

The paper develops a wreath-product account of recurrent-language-model expressivity and shows why arithmetic semantics matter: fixed floating-point recurrences and unsigned-integer wraparound can have different formal-language capabilities.

## Release status

The evidence-release gate **PASSED**: all three live claims receive the full declared `6/6` points. The overall result is **VERIFIED_SCOPED**. The strict paper-level gate remains **NOT_READY** because the clean-room checks are finite witnesses and controls; they do not establish every universal theorem or survey claim by enumeration. No author executable was found in the accepted source.

`VERIFIED_SCOPED` means that the pinned source anchors, exact finite constructions, arithmetic controls, and dependency checks pass. It does not claim that a small finite chain is IEEE floating point or that the repository reimplements every architecture discussed in the paper.

| Claim | Paper statement | Status | Claim producer and evidence |
| --- | --- | --- | --- |
| C1 | Wreath products unify expressivity analysis across recurrent models | **VERIFIED_SCOPED** | `repro/src/full_audit.py::claim_1_wreath_factorization`; exact two-layer realized wreath factorization over four states, with an ambient-reset negative control in `outputs/audit.json` |
| C2 | Deterministic finite-precision semantics enable rigorous analysis | **VERIFIED_SCOPED** | `repro/src/full_audit.py::claim_2_finite_precision`; three finite ordered domains, exhaustive nonnegative update monoids, signed-cycle control, and Float32 evaluation-order control |
| C3 | Representative RNN/LSTM/SSM expressivity claims can be corrected | **VERIFIED_SCOPED** | `repro/src/full_audit.py::claim_3_semantics_correction`; 4-bit unsigned-wraparound parity construction exhaustively checks 2,047 words through length 10 and contrasts fixed floating-point semantics |

## How each claim is produced

```text
arXiv source + live contract pin
  → dependency-free finite transformation audit
  → arithmetic-semantic controls and exact witnesses
  → reproducibility test + hash-addressed evidence bundle
  → fail-closed publication gate
```

### C1 — realized wreath factorization

`full_audit.py` constructs a two-layer recurrence on four states. For each input token, it factors the realized transition through the left wreath action, and the generated realized transition monoid has size `8`. A reset transformation present only in an ambient lower monoid is rejected, preserving the paper's realized-versus-ambient distinction.

Supplemental [Proposition 3.20 cascade audit](pages/claim-2-proposition-3-20-exact/page.md) checks the Appendix-F dependency chain, 144 canonical regroupings, 12 projection witnesses, and 15 independent projection cases. It is a proof-chain audit under the proposition's hypotheses, not a finite-sample extrapolation.

### C2 — fixed finite-precision semantics

The audit enumerates nonnegative saturated affine updates on ordered domains of widths `3`, `5`, and `7`. Their generated transformation monoids are aperiodic with sizes `10`, `82`, and `377`. Two controls are retained: a signed multiplier creates a rejected two-cycle, and Float32 reassociation yields `(a+b)+c=0` versus `a+(b+c)=1`, proving that evaluation order is part of the declared semantics.

The finite-chain audit is a witness for the mechanism; it is not mislabeled as an IEEE floating-point theorem.

### C3 — unsigned parity correction

The audit implements the source's 4-bit unsigned-wraparound recurrence with `A=1`, `B(0)=0`, `B(1)=8`, initial state `15`, and acceptance `{15}`. It accepts exactly the even-parity binary words across all `2,047` words of lengths `0` through `10`, and its transition monoid contains a nontrivial `C2`. A boundary control records that this construction has order `2`; no mod-3 claim is made.

The result is contrasted with the fixed floating-point, nonnegative aperiodicity setting. The arithmetic model is part of the claim and is never silently changed.

## Branch map

The repository has one final branch:

| Final branch | Former branch | Purpose |
| --- | --- | --- |
| `main` | `main` | Canonical source pin, claim audit, supplemental Proposition 3.20 certificate, citation, and release metadata |

See [BRANCH_AUDIT.md](BRANCH_AUDIT.md) for the final ref check.

## Pinned inputs and provenance

- Paper: [arXiv:2606.01765v2](https://arxiv.org/abs/2606.01765); OpenReview identifier `7pbmZatDuD`.
- Source archive: `docs/arxiv_source.tar`, SHA-256 `0c2c76a4c00dd05344ed167f19cda265918edb47112a95884c7f9c55bb985790`.
- Primary PDF: `docs/primary.pdf`, SHA-256 `2437886679ac4c76b60d008dce1da217abe7a96bbdac77298660c2e82832071e`.
- Primary TeX: `docs/source/main.tex`, SHA-256 `705d5e48e81819fd802fe12f0c3b54d8769bd0ec0cf5becf7f274096ba63dd6c`.
- Official author executable: none found in the accepted source; this is a clean-room audit.

## Reproduce the audit

No external package or GPU is required:

```bash
git clone https://github.com/MachineLearning-Nerd/icml26-algebraic-rnn-expressivity.git
cd icml26-algebraic-rnn-expressivity
python3 repro/src/full_audit.py --output outputs/audit.json
python3 repro/src/run_tests.py
python3 repro/src/verify_claims.py
python3 repro/src/verify_prop_3_20_exact.py
python3 repro/src/audit_prop_3_20_exact.py
python3 repro/src/build_evidence_bundle.py
```

The scripts fail closed on source-pin mismatch, missing contract fields, failed controls, or incomplete claims. The evidence bundle records SHA-256 values for the source, contract, producer scripts, tests, and release documents.

## Documentation

- [Evidence ledger](docs/EVIDENCE.md)
- [Source audit](docs/SOURCE_AUDIT.md)
- [Source manifest and citation](SOURCE_MANIFEST.md)
- [Audit report](AUDIT_REPORT.md)
- [Branch audit](BRANCH_AUDIT.md)
- [Publication gate](docs/PUBLICATION_GATE.md)
- [Output guide](outputs/README.md)
- [Supplemental Proposition 3.20 page](pages/claim-2-proposition-3-20-exact/page.md)

## Citation

```bibtex
@article{nowak2026algebraic,
  title={An Algebraic View of the Expressivity of Recurrent Language Models},
  author={Nowak, Franz and Cotterell, Ryan and Boumasmoud, Reda},
  journal={arXiv preprint arXiv:2606.01765},
  year={2026},
  note={ICML 2026}
}
```

Paper page: [arXiv:2606.01765v2](https://arxiv.org/abs/2606.01765).

## Thank you

Thank you to Franz Nowak, Ryan Cotterell, and Reda Boumasmoud for giving the expressivity discussion a precise algebraic language and for making the arithmetic assumptions explicit. That clarity makes it possible to audit realized wreath structure, finite-precision evaluation order, and unsigned-wraparound counterexamples without hiding the scope boundaries.

Maintained by [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd).
