# Negative controls


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_ca17bb7a980f", "created_at": "2026-07-20T10:22:23+00:00", "title": "Controls that must fail"}
-->
The audit rejects (1) treating an ambient reset as a realized input transition, (2) dropping the nonnegative-multiplier condition because negation has order two, (3) regrouping Float32 arithmetic because 1 + 2^24 - 2^24 changes from 0 to 1 by grouping, and (4) overextending the parity witness to mod-3.
