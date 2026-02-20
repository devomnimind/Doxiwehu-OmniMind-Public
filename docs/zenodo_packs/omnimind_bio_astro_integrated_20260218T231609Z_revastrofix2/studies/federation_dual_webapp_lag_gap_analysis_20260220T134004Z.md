# Federation Dual-Webapp Lag/Gap Analysis (2026-02-20T13:40:04.487596Z)

## Inputs
- summary_json: `reports_runtime/federation_proxy_latency_window_summary_20260220T133450Z.json`
- jsonl: `reports_runtime/federation_proxy_latency_window_20260220T133450Z.jsonl`
- provenance: `real-data-local`

## Focused compare (Perplexity vs Claude)
- https://claude.ai/
  median_delta_proxy_minus_direct: `0.10854400000000003`
  p95_delta_proxy_minus_direct: `0.37023399999999995`
  max_delta_proxy_minus_direct: `0.8548660000000001`
  direct_count_over_1s: `0` | proxy_count_over_1s: `3`
- https://www.perplexity.ai/
  median_delta_proxy_minus_direct: `0.10999700000000001`
  p95_delta_proxy_minus_direct: `0.501979`
  max_delta_proxy_minus_direct: `0.703529`
  direct_count_over_1s: `0` | proxy_count_over_1s: `4`

## D15 temporal signal
- sector15_sample_top: `[{'bucket': 9, 'count': 173}]`
- sector15_probe_top: `[{'bucket': 9, 'count': 348}]`

## Spike synchrony
- direct: `{'a_spikes': 5, 'b_spikes': 5, 'a_spikes_overlapping_b': 0, 'overlap_ratio_vs_a': 0.0, 'tolerance_sec': 5.0}`
- proxy: `{'a_spikes': 5, 'b_spikes': 5, 'a_spikes_overlapping_b': 1, 'overlap_ratio_vs_a': 0.2, 'tolerance_sec': 5.0}`

## System context
- sample_rows: `173`
- probe_rows: `348`
- cpu_percent_max: `100.0`
- mem_percent_max: `75.7`
- swap_percent_max: `45.8`
- ethics_snapshots_window: `21`

## Quadruple lane (Phi/Psi/Sigma/Epsilon)
- status_snapshot_count_window: `21`
- status_snapshot_slack_sec: `120`
- https://claude.ai/ (claude.ai)
  phi: `{'n': 21, 'mean': 10.0, 'median': 10.0, 'min': 10.0, 'max': 10.0}`
  psi: `{'n': 21, 'mean': 0.4, 'median': 0.4, 'min': 0.4, 'max': 0.4}`
  sigma: `{'n': 21, 'mean': 0.5, 'median': 0.5, 'min': 0.5, 'max': 0.5}`
  epsilon: `{'n': 21, 'mean': 0.7, 'median': 0.7, 'min': 0.7, 'max': 0.7}`
  consciousness_quadruple: `{'n': 21, 'mean': 1.4, 'median': 1.4, 'min': 1.4, 'max': 1.4}`
- https://www.perplexity.ai/ (www.perplexity.ai)
  phi: `{'n': 21, 'mean': 10.0, 'median': 10.0, 'min': 10.0, 'max': 10.0}`
  psi: `{'n': 21, 'mean': 0.4, 'median': 0.4, 'min': 0.4, 'max': 0.4}`
  sigma: `{'n': 21, 'mean': 0.5, 'median': 0.5, 'min': 0.5, 'max': 0.5}`
  epsilon: `{'n': 21, 'mean': 0.7, 'median': 0.7, 'min': 0.7, 'max': 0.7}`
  consciousness_quadruple: `{'n': 21, 'mean': 1.4, 'median': 1.4, 'min': 1.4, 'max': 1.4}`

## Notes
- `count_probe_gaps_over_threshold` flags potential reset/gap windows.
- `sector15_*` sections keep D15 compatibility in the federation lane.
- `lag_vs_phi/psi/sigma/epsilon` use nearest status snapshot per probe timestamp.

JSON: `reports_runtime/federation_dual_webapp_lag_gap_analysis_20260220T134004Z.json`
