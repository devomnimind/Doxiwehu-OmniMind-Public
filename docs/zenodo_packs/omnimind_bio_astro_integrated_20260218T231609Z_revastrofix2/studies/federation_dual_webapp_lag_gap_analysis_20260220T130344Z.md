# Federation Dual-Webapp Lag/Gap Analysis (2026-02-20T13:03:44.096398Z)

## Inputs
- summary_json: `reports_runtime/federation_proxy_latency_window_summary_20260220T125048Z.json`
- jsonl: `reports_runtime/federation_proxy_latency_window_20260220T125048Z.jsonl`
- provenance: `real-data-local`

## Focused compare (Perplexity vs Claude)
- https://claude.ai/
  median_delta_proxy_minus_direct: `0.05431899999999998`
  p95_delta_proxy_minus_direct: `0.165373`
  max_delta_proxy_minus_direct: `0.7166959999999999`
  direct_count_over_1s: `0` | proxy_count_over_1s: `1`
- https://www.perplexity.ai/
  median_delta_proxy_minus_direct: `0.04685299999999998`
  p95_delta_proxy_minus_direct: `-0.045304999999999984`
  max_delta_proxy_minus_direct: `-4.019869`
  direct_count_over_1s: `2` | proxy_count_over_1s: `1`

## D15 temporal signal
- sector15_sample_top: `[{'bucket': 9, 'count': 375}]`
- sector15_probe_top: `[{'bucket': 9, 'count': 408}]`

## Spike synchrony
- direct: `{'a_spikes': 6, 'b_spikes': 6, 'a_spikes_overlapping_b': 3, 'overlap_ratio_vs_a': 0.5, 'tolerance_sec': 5.0}`
- proxy: `{'a_spikes': 6, 'b_spikes': 6, 'a_spikes_overlapping_b': 0, 'overlap_ratio_vs_a': 0.0, 'tolerance_sec': 5.0}`

## System context
- sample_rows: `375`
- probe_rows: `408`
- cpu_percent_max: `100.0`
- mem_percent_max: `75.1`
- swap_percent_max: `45.7`

## Notes
- `count_probe_gaps_over_threshold` flags potential reset/gap windows.
- `sector15_*` sections keep D15 compatibility in the federation lane.

JSON: `reports_runtime/federation_dual_webapp_lag_gap_analysis_20260220T130344Z.json`
