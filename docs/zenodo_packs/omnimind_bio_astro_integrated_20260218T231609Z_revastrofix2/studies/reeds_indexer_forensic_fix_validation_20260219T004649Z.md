# Reeds Indexer Forensic Fix Validation (20260219T004649Z)

- status: `OK_LOCAL_FIXED`
- collection: `kb_reeds_neurais`
- points: `124`

## Root cause
index_reeds_neurais.py passed is_forensic=True but DatasetIndexer.index_dataset lacked this parameter, causing TypeError and abort.

## Fix applied
- DatasetIndexer now accepts is_forensic/allow_interest/use_ethical_filters kwargs.
- HDF5 (.h5/.hdf5) summarization path added via h5py metadata extraction.
- Ethical+topological decisions logged per chunk and stored in payload.
- Forensic mode preserves auditability (bypass for denied classes, with decision trace).

## Sample decision counts (first 500 points)
- resonance: `{'accept': 124}`
- topological: `{'interest': 124}`

JSON: `/home/fahbrain/projects/omnimind/reports_runtime/reeds_indexer_forensic_fix_validation_20260219T004649Z.json`
