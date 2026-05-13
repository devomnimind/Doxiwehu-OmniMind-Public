# Reeds Interest Gate A/B Validation (20260219T005334Z)

- nonforensic_no_interest: collection=`kb_reeds_probe_nonforensic` count=`0` accepted_chunks=`0`
- nonforensic_allow_interest: collection=`kb_reeds_probe_interest` count=`2` accepted_chunks=`2`
- forensic_no_interest: collection=`kb_reeds_probe_forensic` count=`2` accepted_chunks=`2`

## Diagnosis
- When topological decision is interest, default non-forensic gate without allow_interest drops chunks (0/N).
- allow_interest=True or is_forensic=True preserves the same chunks.
- Observed zero-ing was gate semantics, not evidence of parser failure.

JSON: `/home/fahbrain/projects/omnimind/reports_runtime/reeds_interest_gate_ab_validation_20260219T005334Z.json`
