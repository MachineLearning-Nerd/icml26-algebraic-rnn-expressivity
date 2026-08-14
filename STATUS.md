# Status — An Algebraic View of Recurrent Language-Model Expressivity

## Current release

- Repository target: `MachineLearning-Nerd/icml26-algebraic-rnn-expressivity`
- Paper: *An Algebraic View of the Expressivity of Recurrent Language Models*
- OpenReview: `7pbmZatDuD`
- arXiv: `2606.01765v2`
- Authors: Franz Nowak, Ryan Cotterell, and Reda Boumasmoud
- Evidence-release gate: **PASSED**
- Overall result: **VERIFIED_SCOPED**
- Strict paper-level gate: **NOT_READY**
- Contract score: **6/6 declared points**
- Author executable found: **no**
- External score claimed: **no**

## Claim status

| Claim | Final status | Scope |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | Exact finite realized wreath factorization and ambient-reset control |
| C2 | `VERIFIED_SCOPED` | Finite ordered-chain aperiodicity and arithmetic-semantics controls |
| C3 | `VERIFIED_SCOPED` | Exact 4-bit unsigned-wraparound parity construction versus floating semantics |

## Evidence boundary

The audit is a clean-room finite witness and control suite. C1 does not survey all RNNs, C2 does not claim that a small saturated chain is IEEE floating point, and C3 is specifically a 4-bit unsigned-wraparound parity correction. The supplemental Proposition 3.20 page checks the universal dependency chain under its stated hypotheses and keeps finite projection witnesses as corroboration rather than proof by sampling.

## Branch hygiene

The final remote has one branch, `main`. Source pins, claim evidence, citation, thank-you note, and release metadata are all on that canonical branch.
