# Evidence ledger

This ledger distinguishes exact finite witnesses, arithmetic controls, and the supplemental proof-chain audit. `VERIFIED_SCOPED` records a passing declared contract; it does not claim that a finite enumeration proves every universal statement in the paper.

## C1 — wreath-product framework

Producer: `repro/src/full_audit.py::claim_1_wreath_factorization`.

The audit constructs a two-layer recurrence over four states, factors both token transitions through the realized left wreath action, and enumerates a realized transition monoid of size `8`. A reset transformation included only in an ambient lower monoid is rejected as unrealized.

Artifact: `outputs/audit.json`.

Result: **VERIFIED_SCOPED** for the explicit finite witness.

Supplemental evidence: `repro/src/verify_prop_3_20_exact.py` validates the Proposition 3.20 dependency chain, 144 canonical regroupings, and 12 projection witnesses; `audit_prop_3_20_exact.py` independently validates 15 additional projection cases.

## C2 — deterministic finite-precision semantics

Producer: `repro/src/full_audit.py::claim_2_finite_precision`.

For ordered domains of widths `3`, `5`, and `7`, the audit enumerates nonnegative saturated affine updates and their generated transformation monoids. The monoid sizes are `10`, `82`, and `377`, with aperiodicity exponents `2`, `4`, and `6`. A signed multiplier creates a rejected two-cycle. A Float32 control gives `(a+b)+c=0` and `a+(b+c)=1`, preserving the source's fixed evaluation-order condition.

Artifact: `outputs/audit.json`.

Result: **VERIFIED_SCOPED** for the finite deterministic semantics and controls.

## C3 — rederivation and correction

Producer: `repro/src/full_audit.py::claim_3_semantics_correction`.

The audit implements the source's 4-bit unsigned-wraparound recurrence with `A=1`, `B(0)=0`, `B(1)=8`, initial state `15`, and accept state `{15}`. It exhaustively checks all `2,047` binary words through length `10`, accepts exactly even parity, and finds a transition monoid of size `2` containing a nontrivial `C2`. The boundary control records that no mod-3 claim is made.

Artifact: `outputs/audit.json`.

Result: **VERIFIED_SCOPED** for the declared unsigned construction and its floating-point contrast.

## Evidence path

```text
source archive + live contract
  → dependency-free exact audit
  → arithmetic and scope controls
  → reproducibility test
  → hash-addressed evidence bundle
  → fail-closed publication gate
```
