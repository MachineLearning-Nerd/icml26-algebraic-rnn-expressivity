# Source audit

## Paper identity

- Paper: [arXiv:2606.01765v2](https://arxiv.org/abs/2606.01765), *An Algebraic View of the Expressivity of Recurrent Language Models*.
- Authors: Franz Nowak, Ryan Cotterell, and Reda Boumasmoud.
- OpenReview identifier: `7pbmZatDuD`.
- Source archive: `docs/arxiv_source.tar`.

## Integrity pins

| Artifact | SHA-256 | Used for |
| --- | --- | --- |
| `docs/arxiv_source.tar` | `0c2c76a4c00dd05344ed167f19cda265918edb47112a95884c7f9c55bb985790` | Complete arXiv source archive |
| `docs/primary.pdf` | `2437886679ac4c76b60d008dce1da217abe7a96bbdac77298660c2e82832071e` | Primary paper readback |
| `docs/source/main.tex` | `705d5e48e81819fd802fe12f0c3b54d8769bd0ec0cf5becf7f274096ba63dd6c` | Claim anchors and definitions |

The hashes are duplicated in `docs/source_pins.json` and checked by `repro/src/full_audit.py` before claim outcomes are accepted. The live contract is pinned in `docs/live_claims_2026-07-20.json` with three claims and six possible points.

## Author-code boundary

No executable author artifact was found in the accepted source. The implementation is clean-room and dependency-free. The source files are retained for anchor inspection, not presented as executable author code.

## Scope boundary

The audit preserves the source assumptions: realized rather than merely ambient wreath products, nonnegative multipliers, NaNs excluded, recurrence-consistent floating-point evaluation order, and explicit unsigned wraparound for the parity construction. It does not replace the paper's general proofs with small finite examples.
