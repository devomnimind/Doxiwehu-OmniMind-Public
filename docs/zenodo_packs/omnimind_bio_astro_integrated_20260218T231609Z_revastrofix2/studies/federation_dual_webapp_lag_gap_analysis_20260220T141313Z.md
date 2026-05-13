# Federation Dual-Webapp Lag/Gap Analysis (2026-02-20T14:13:13.282178Z)

## Inputs
- summary_json: `reports_runtime/federation_proxy_latency_window_summary_20260220T140555Z.json`
- jsonl: `reports_runtime/federation_proxy_latency_window_20260220T140555Z.jsonl`
- provenance: `real-data-local`

## Focused compare (Perplexity vs Claude)
- https://claude.ai/
  median_delta_proxy_minus_direct: `0.05496400000000001`
  p95_delta_proxy_minus_direct: `0.17114400000000007`
  max_delta_proxy_minus_direct: `1.892087`
  direct_count_over_1s: `0` | proxy_count_over_1s: `4`
  lag_vs_cpu_pearson: `-0.27253056437591816`
  lag_vs_depth60s_pearson: `None`
  lag_vs_size_download_pearson: `0.09441075894177939`
- https://www.perplexity.ai/
  median_delta_proxy_minus_direct: `0.04796400000000001`
  p95_delta_proxy_minus_direct: `0.09936500000000004`
  max_delta_proxy_minus_direct: `0.83632`
  direct_count_over_1s: `0` | proxy_count_over_1s: `2`
  lag_vs_cpu_pearson: `-0.11634260795018125`
  lag_vs_depth60s_pearson: `None`
  lag_vs_size_download_pearson: `-0.06964933619440675`

## D15 temporal signal
- sector15_sample_top: `[{'bucket': 9, 'count': 251}]`
- sector15_probe_top: `[{'bucket': 9, 'count': 504}]`

## Spike synchrony
- direct: `{'a_spikes': 7, 'b_spikes': 7, 'a_spikes_overlapping_b': 0, 'overlap_ratio_vs_a': 0.0, 'tolerance_sec': 5.0}`
- proxy: `{'a_spikes': 7, 'b_spikes': 7, 'a_spikes_overlapping_b': 2, 'overlap_ratio_vs_a': 0.2857142857142857, 'tolerance_sec': 5.0}`

## System context
- sample_rows: `251`
- probe_rows: `504`
- cpu_percent_max: `100.0`
- mem_percent_max: `77.5`
- swap_percent_max: `45.9`
- ethics_snapshots_window: `28`

## Quadruple lane (Phi/Psi/Sigma/Epsilon)
- status_snapshot_count_window: `28`
- status_snapshot_slack_sec: `120`
- https://claude.ai/ (claude.ai)
  phi: `{'n': 28, 'mean': 10.0, 'median': 10.0, 'min': 10.0, 'max': 10.0}`
  psi: `{'n': 28, 'mean': 0.4, 'median': 0.4, 'min': 0.4, 'max': 0.4}`
  sigma: `{'n': 28, 'mean': 0.5, 'median': 0.5, 'min': 0.5, 'max': 0.5}`
  epsilon: `{'n': 28, 'mean': 0.7, 'median': 0.7, 'min': 0.7, 'max': 0.7}`
  consciousness_quadruple: `{'n': 28, 'mean': 1.4, 'median': 1.4, 'min': 1.4, 'max': 1.4}`
- https://www.perplexity.ai/ (www.perplexity.ai)
  phi: `{'n': 28, 'mean': 10.0, 'median': 10.0, 'min': 10.0, 'max': 10.0}`
  psi: `{'n': 28, 'mean': 0.4, 'median': 0.4, 'min': 0.4, 'max': 0.4}`
  sigma: `{'n': 28, 'mean': 0.5, 'median': 0.5, 'min': 0.5, 'max': 0.5}`
  epsilon: `{'n': 28, 'mean': 0.7, 'median': 0.7, 'min': 0.7, 'max': 0.7}`
  consciousness_quadruple: `{'n': 28, 'mean': 1.4, 'median': 1.4, 'min': 1.4, 'max': 1.4}`

## Witness lane (session depth)
- depth_window_sec: `60.0`

## Depth/Size lane (per series)
- https://claude.ai/|direct
  response_size_bytes: `{'n': 126, 'mean': 7035.166666666667, 'median': 7037.0, 'min': 6995.0, 'max': 7059.0}`
  witness_depth60s: `{'n': 126, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 126, 'bins': [{'bin': 'low', 'n': 42, 'signal_range': [6995.0, 7037.0], 'lag_mean': 0.20235402380952378, 'lag_median': 0.16725299999999999}, {'bin': 'mid', 'n': 42, 'signal_range': [7037.0, 7037.0], 'lag_mean': 0.18071445238095238, 'lag_median': 0.16429749999999999}, {'bin': 'high', 'n': 42, 'signal_range': [7037.0, 7059.0], 'lag_mean': 0.1897854523809524, 'lag_median': 0.1660965}]}`
  lag_by_depth60s_terciles: `{'n': 126, 'bins': [{'bin': 'low', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.1981585, 'lag_median': 0.1721985}, {'bin': 'mid', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.1841550476190476, 'lag_median': 0.15998}, {'bin': 'high', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.19054038095238096, 'lag_median': 0.171571}]}`
- https://claude.ai/|proxy
  response_size_bytes: `{'n': 126, 'mean': 9197.02380952381, 'median': 9192.0, 'min': 9150.0, 'max': 9235.0}`
  witness_depth60s: `{'n': 126, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 126, 'bins': [{'bin': 'low', 'n': 42, 'signal_range': [9150.0, 9192.0], 'lag_mean': 0.3567832380952381, 'lag_median': 0.2432905}, {'bin': 'mid', 'n': 42, 'signal_range': [9192.0, 9214.0], 'lag_mean': 0.24819385714285713, 'lag_median': 0.2125395}, {'bin': 'high', 'n': 42, 'signal_range': [9214.0, 9235.0], 'lag_mean': 0.34930288095238093, 'lag_median': 0.2091145}]}`
  lag_by_depth60s_terciles: `{'n': 126, 'bins': [{'bin': 'low', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.47188038095238094, 'lag_median': 0.279878}, {'bin': 'mid', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.24697400000000003, 'lag_median': 0.2121015}, {'bin': 'high', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.23542559523809523, 'lag_median': 0.20767000000000002}]}`
- https://www.perplexity.ai/|direct
  response_size_bytes: `{'n': 126, 'mean': 7051.230158730159, 'median': 7045.0, 'min': 7003.0, 'max': 7088.0}`
  witness_depth60s: `{'n': 126, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 126, 'bins': [{'bin': 'low', 'n': 42, 'signal_range': [7003.0, 7045.0], 'lag_mean': 0.21635359523809522, 'lag_median': 0.1738945}, {'bin': 'mid', 'n': 42, 'signal_range': [7045.0, 7067.0], 'lag_mean': 0.20911214285714286, 'lag_median': 0.17469200000000001}, {'bin': 'high', 'n': 42, 'signal_range': [7067.0, 7088.0], 'lag_mean': 0.175676, 'lag_median': 0.1723615}]}`
  lag_by_depth60s_terciles: `{'n': 126, 'bins': [{'bin': 'low', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2061735, 'lag_median': 0.1818225}, {'bin': 'mid', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.19994295238095236, 'lag_median': 0.179815}, {'bin': 'high', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.19502528571428573, 'lag_median': 0.1641065}]}`
- https://www.perplexity.ai/|proxy
  response_size_bytes: `{'n': 126, 'mean': 9214.095238095239, 'median': 9222.0, 'min': 9158.0, 'max': 9264.0}`
  witness_depth60s: `{'n': 126, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 126, 'bins': [{'bin': 'low', 'n': 42, 'signal_range': [9158.0, 9200.0], 'lag_mean': 0.30504988095238095, 'lag_median': 0.2567065}, {'bin': 'mid', 'n': 42, 'signal_range': [9200.0, 9222.0], 'lag_mean': 0.2835152619047619, 'lag_median': 0.2129185}, {'bin': 'high', 'n': 42, 'signal_range': [9222.0, 9264.0], 'lag_mean': 0.2470095238095238, 'lag_median': 0.2183785}]}`
  lag_by_depth60s_terciles: `{'n': 126, 'bins': [{'bin': 'low', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.3680770952380953, 'lag_median': 0.2717545}, {'bin': 'mid', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2247745714285714, 'lag_median': 0.19515100000000002}, {'bin': 'high', 'n': 42, 'signal_range': [0.0, 0.0], 'lag_mean': 0.24272300000000002, 'lag_median': 0.21676600000000001}]}`

## Notes
- `count_probe_gaps_over_threshold` flags potential reset/gap windows.
- `sector15_*` sections keep D15 compatibility in the federation lane.
- `lag_vs_phi/psi/sigma/epsilon` use nearest status snapshot per probe timestamp.

JSON: `reports_runtime/federation_dual_webapp_lag_gap_analysis_20260220T141313Z.json`
