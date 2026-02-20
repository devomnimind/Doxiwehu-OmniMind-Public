# Reeds Topological Filter Behavior Diagnosis (20260219T004056Z)

- sample_h5: `/media/fahbrain/DEV_BRAIN_CLEAN/omnimind_knowledge/temp_deglutition/reeds_neurais_extracted/central_obsdata_uchuumod.h5`
- chunks_total: `1`
- resonance_decisions: `{'accept': 1}`
- topological_decisions: `{'interest': 1}`
- accepted_by_current_gate: `0`

## Key diagnosis
- Topological filter is active and can classify neutral technical metadata as interest when no lexical noise/care pattern dominates.
- Current DatasetIndexer gate accepts only topological decisions accept/protect_only; interest is dropped.
- Therefore 0/N can occur without explicit violence detection; it is a gate policy effect, not necessarily a false violence hit.

JSON: `reports_runtime/reeds_topological_filter_behavior_diagnosis_20260219T004056Z.json`
