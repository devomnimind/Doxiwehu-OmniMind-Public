# HF Realdata Integration Status

## Before (17/02)
- mode: `metadata`
- model_mode: `metadata`
- pulled_items: `17`
- characterization: metadata-only (predominantly README/config).

## After (agora)
- qdrant_collection: `hf_realdata_samples_live`
- qdrant_points: `1338`
- parquet_rows_ingested: `829`
- csv_rows_ingested: `500`

## Pending deep ingest candidates
- `ibm-nasa-geospatial/Prithvi-WxC-1.0-2300M`: strong_data_signal_but_no_data_ok_in_local_sample
- `nohurry/Opus-4.6-Reasoning-3000x-filtered`: strong_data_signal_but_no_data_ok_in_local_sample
- `TeichAI/gemini-3-pro-preview-high-reasoning-1000x`: strong_data_signal_but_no_data_ok_in_local_sample

JSON: `reports_runtime/hf_realdata_integration_status_20260219T114854Z.json`
