# Federation Webapp Metrics + D15 Status

## Real capture completed
- window: `2026-02-20T12:37:43.343859Z` to `2026-02-20T12:42:44.361380Z`
- events: `329` lines in `reports_runtime/federation_proxy_latency_window_20260220T123743Z.jsonl`
- outputs:
  - `reports_runtime/federation_proxy_latency_window_summary_20260220T123743Z.json`
  - `reports_runtime/federation_proxy_latency_window_summary_20260220T123743Z.md`
  - `output/img/federation_proxy_latency_window_20260220T123743Z/latency_timeseries.png`

## Measured proxy overhead (median)
- perplexity: `+0.050619 s`
- zenodo: `+0.0953065 s`
- github: `+0.0309645 s`

## Runtime peaks in same window
- CPU max: `99.9%`
- MEM max: `74.1%`
- SWAP max: `45.6%`

## D12->D15 compatibility updates
- `src/consciousness/api_reset_detector.py`: reset events now include `sector15_tod`; stats include `resets_by_sector15`.
- `scripts/analysis/build_federation_social_dataset.py`: social payloads now include `sector15_tod` plus existing `house12_2h`.
- `scripts/analysis/capture_federation_proxy_latency_window.py`: keeps `sector15_tod` and fixed proxy CA handling.

## Provenance
- `real-data-local`
