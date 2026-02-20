# Federation Dual-Webapp Lag/Gap Analysis (2026-02-20T13:12:57.842155Z)

## Inputs
- summary_json: `reports_runtime/federation_proxy_latency_window_summary_20260220T130745Z.json`
- jsonl: `reports_runtime/federation_proxy_latency_window_20260220T130745Z.jsonl`
- provenance: `real-data-local`

## Focused compare (Perplexity vs Claude)
- https://claude.ai/
  median_delta_proxy_minus_direct: `0.06670299999999996`
  p95_delta_proxy_minus_direct: `0.190249`
  max_delta_proxy_minus_direct: `0.733228`
  direct_count_over_1s: `0` | proxy_count_over_1s: `1`
- https://www.perplexity.ai/
  median_delta_proxy_minus_direct: `0.046176999999999996`
  p95_delta_proxy_minus_direct: `0.44856299999999993`
  max_delta_proxy_minus_direct: `1.644339`
  direct_count_over_1s: `0` | proxy_count_over_1s: `3`

## D15 temporal signal
- sector15_sample_top: `[{'bucket': 9, 'count': 321}]`
- sector15_probe_top: `[{'bucket': 9, 'count': 344}]`

## Spike synchrony
- direct: `{'a_spikes': 5, 'b_spikes': 5, 'a_spikes_overlapping_b': 0, 'overlap_ratio_vs_a': 0.0, 'tolerance_sec': 5.0}`
- proxy: `{'a_spikes': 5, 'b_spikes': 5, 'a_spikes_overlapping_b': 1, 'overlap_ratio_vs_a': 0.2, 'tolerance_sec': 5.0}`

## System context
- sample_rows: `321`
- probe_rows: `344`
- cpu_percent_max: `100.0`
- mem_percent_max: `74.7`
- swap_percent_max: `45.9`

## Notes
- `count_probe_gaps_over_threshold` flags potential reset/gap windows.
- `sector15_*` sections keep D15 compatibility in the federation lane.

JSON: `reports_runtime/federation_dual_webapp_lag_gap_analysis_20260220T131257Z.json`
