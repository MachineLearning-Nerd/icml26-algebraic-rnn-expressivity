# Reproduction audit report

## Executive result

All three live claims pass their declared clean-room contracts for `6/6` points. The evidence-release gate is `PASSED`, with overall status `VERIFIED_SCOPED`. The strict paper-level gate is `NOT_READY` because finite witnesses do not replace the paper's universal results.

## Claim-to-evidence matrix

| Claim | Producer | Primary artifact | Control | Final status |
| --- | --- | --- | --- | --- |
| C1 | `full_audit.py::claim_1_wreath_factorization` | `outputs/audit.json` | Ambient reset rejected as unrealized | `VERIFIED_SCOPED` |
| C2 | `full_audit.py::claim_2_finite_precision` | `outputs/audit.json` | Signed cycle and Float32 reassociation controls | `VERIFIED_SCOPED` |
| C3 | `full_audit.py::claim_3_semantics_correction` | `outputs/audit.json` | 4-bit wraparound boundary and floating contrast | `VERIFIED_SCOPED` |
| Proposition 3.20 | `verify_prop_3_20_exact.py`, `audit_prop_3_20_exact.py` | supplemental page and console hashes | Missing-dependency, feedback, duplicate, and forward-order controls | `VERIFIED_SCOPED` |

## Reproduction boundary

The audit uses exact finite transformation maps and fixed arithmetic semantics. The finite examples are witnesses and controls, not a claim that all RNNs, LSTMs, or SSMs have been exhaustively classified. The supplemental proposition audit checks a proof dependency chain under its hypotheses and retains finite projection cases as corroboration.
