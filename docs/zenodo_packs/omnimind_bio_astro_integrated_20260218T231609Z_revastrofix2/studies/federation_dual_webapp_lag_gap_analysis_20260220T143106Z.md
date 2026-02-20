# Federation Dual-Webapp Lag/Gap Analysis (2026-02-20T14:31:06.767651Z)

## Inputs
- summary_json: `reports_runtime/federation_proxy_latency_window_summary_20260220T142553Z.json`
- jsonl: `reports_runtime/federation_proxy_latency_window_20260220T142553Z.jsonl`
- provenance: `real-data-local`

## Focused compare (Perplexity vs Claude)
- https://claude.ai/
  median_delta_proxy_minus_direct: `0.07430349999999997`
  p95_delta_proxy_minus_direct: `0.23450199999999993`
  max_delta_proxy_minus_direct: `0.7803740000000001`
  direct_count_over_1s: `0` | proxy_count_over_1s: `2`
  lag_vs_cpu_pearson: `0.2893225643153821`
  lag_vs_depth60s_pearson: `None`
  lag_vs_size_download_pearson: `-0.05625258246476053`
  lag_vs_session_progress_pearson: `0.25562302094211276`
  lag_vs_conversation_depth180s_pearson: `None`
  lag_vs_last_text_len_pearson: `None`
- https://www.perplexity.ai/
  median_delta_proxy_minus_direct: `0.07651249999999998`
  p95_delta_proxy_minus_direct: `0.09160400000000002`
  max_delta_proxy_minus_direct: `1.023104`
  direct_count_over_1s: `0` | proxy_count_over_1s: `2`
  lag_vs_cpu_pearson: `0.1795691677572878`
  lag_vs_depth60s_pearson: `None`
  lag_vs_size_download_pearson: `0.10783628326987`
  lag_vs_session_progress_pearson: `0.4086652380806333`
  lag_vs_conversation_depth180s_pearson: `None`
  lag_vs_last_text_len_pearson: `None`

## D15 temporal signal
- sector15_sample_top: `[{'bucket': 10, 'count': 171}]`
- sector15_probe_top: `[{'bucket': 10, 'count': 344}]`

## Spike synchrony
- direct: `{'a_spikes': 5, 'b_spikes': 5, 'a_spikes_overlapping_b': 0, 'overlap_ratio_vs_a': 0.0, 'tolerance_sec': 5.0}`
- proxy: `{'a_spikes': 5, 'b_spikes': 5, 'a_spikes_overlapping_b': 0, 'overlap_ratio_vs_a': 0.0, 'tolerance_sec': 5.0}`

## System context
- sample_rows: `171`
- probe_rows: `344`
- cpu_percent_max: `100.0`
- mem_percent_max: `79.3`
- swap_percent_max: `46.4`
- ethics_snapshots_window: `22`

## Quadruple lane (Phi/Psi/Sigma/Epsilon)
- status_snapshot_count_window: `22`
- status_snapshot_slack_sec: `120`
- https://claude.ai/ (claude.ai)
  phi: `{'n': 22, 'mean': 10.0, 'median': 10.0, 'min': 10.0, 'max': 10.0}`
  psi: `{'n': 22, 'mean': 0.4, 'median': 0.4, 'min': 0.4, 'max': 0.4}`
  sigma: `{'n': 22, 'mean': 0.5, 'median': 0.5, 'min': 0.5, 'max': 0.5}`
  epsilon: `{'n': 22, 'mean': 0.7, 'median': 0.7, 'min': 0.7, 'max': 0.7}`
  consciousness_quadruple: `{'n': 22, 'mean': 1.4, 'median': 1.4, 'min': 1.4, 'max': 1.4}`
- https://www.perplexity.ai/ (www.perplexity.ai)
  phi: `{'n': 22, 'mean': 10.0, 'median': 10.0, 'min': 10.0, 'max': 10.0}`
  psi: `{'n': 22, 'mean': 0.4, 'median': 0.4, 'min': 0.4, 'max': 0.4}`
  sigma: `{'n': 22, 'mean': 0.5, 'median': 0.5, 'min': 0.5, 'max': 0.5}`
  epsilon: `{'n': 22, 'mean': 0.7, 'median': 0.7, 'min': 0.7, 'max': 0.7}`
  consciousness_quadruple: `{'n': 22, 'mean': 1.4, 'median': 1.4, 'min': 1.4, 'max': 1.4}`

## Witness lane (session depth)
- depth_window_sec: `60.0`

## Conversation lane (optional text stream)
- source_jsonl: ``
- depth_window_sec: `180.0`

## Depth/Size lane (per series)
- https://claude.ai/|direct
  response_size_bytes: `{'n': 86, 'mean': 7034.941860465116, 'median': 7037.0, 'min': 6995.0, 'max': 7059.0}`
  witness_depth60s: `{'n': 86, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [6995.0, 7037.0], 'lag_mean': 0.22794078571428572, 'lag_median': 0.195268}, {'bin': 'mid', 'n': 29, 'signal_range': [7037.0, 7037.0], 'lag_mean': 0.23005503448275863, 'lag_median': 0.199344}, {'bin': 'high', 'n': 29, 'signal_range': [7037.0, 7059.0], 'lag_mean': 0.2163934827586207, 'lag_median': 0.194485}]}`
  lag_by_depth60s_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2332222857142857, 'lag_median': 0.19777050000000002}, {'bin': 'mid', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2270736551724138, 'lag_median': 0.199344}, {'bin': 'high', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.21427548275862068, 'lag_median': 0.194485}]}`
  lag_by_session_progress_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.3176470588235294], 'lag_mean': 0.2332222857142857, 'lag_median': 0.19777050000000002}, {'bin': 'mid', 'n': 29, 'signal_range': [0.32941176470588235, 0.6588235294117647], 'lag_mean': 0.2270736551724138, 'lag_median': 0.199344}, {'bin': 'high', 'n': 29, 'signal_range': [0.6705882352941176, 1.0], 'lag_mean': 0.21427548275862068, 'lag_median': 0.194485}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2332222857142857, 'lag_median': 0.19777050000000002}, {'bin': 'mid', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2270736551724138, 'lag_median': 0.199344}, {'bin': 'high', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.21427548275862068, 'lag_median': 0.194485}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`
- https://claude.ai/|proxy
  response_size_bytes: `{'n': 86, 'mean': 9193.941860465116, 'median': 9192.0, 'min': 9150.0, 'max': 9235.0}`
  witness_depth60s: `{'n': 86, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [9150.0, 9192.0], 'lag_mean': 0.349714, 'lag_median': 0.250625}, {'bin': 'mid', 'n': 29, 'signal_range': [9192.0, 9192.0], 'lag_mean': 0.2863609310344828, 'lag_median': 0.242502}, {'bin': 'high', 'n': 29, 'signal_range': [9192.0, 9235.0], 'lag_mean': 0.36345510344827586, 'lag_median': 0.304191}]}`
  lag_by_depth60s_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.0], 'lag_mean': 0.29550496428571427, 'lag_median': 0.225851}, {'bin': 'mid', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.29859575862068966, 'lag_median': 0.283214}, {'bin': 'high', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.4035600344827586, 'lag_median': 0.379168}]}`
  lag_by_session_progress_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.3176470588235294], 'lag_mean': 0.29550496428571427, 'lag_median': 0.225851}, {'bin': 'mid', 'n': 29, 'signal_range': [0.32941176470588235, 0.6588235294117647], 'lag_mean': 0.29859575862068966, 'lag_median': 0.283214}, {'bin': 'high', 'n': 29, 'signal_range': [0.6705882352941176, 1.0], 'lag_mean': 0.4035600344827586, 'lag_median': 0.379168}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.0], 'lag_mean': 0.29550496428571427, 'lag_median': 0.225851}, {'bin': 'mid', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.29859575862068966, 'lag_median': 0.283214}, {'bin': 'high', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.4035600344827586, 'lag_median': 0.379168}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`
- https://www.perplexity.ai/|direct
  response_size_bytes: `{'n': 86, 'mean': 7051.523255813953, 'median': 7045.0, 'min': 6982.0, 'max': 7067.0}`
  witness_depth60s: `{'n': 86, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [6982.0, 7045.0], 'lag_mean': 0.21244039285714283, 'lag_median': 0.172787}, {'bin': 'mid', 'n': 29, 'signal_range': [7045.0, 7067.0], 'lag_mean': 0.23966855172413795, 'lag_median': 0.181064}, {'bin': 'high', 'n': 29, 'signal_range': [7067.0, 7067.0], 'lag_mean': 0.2160231724137931, 'lag_median': 0.209324}]}`
  lag_by_depth60s_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2064123214285714, 'lag_median': 0.1640445}, {'bin': 'mid', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.216578, 'lag_median': 0.186297}, {'bin': 'high', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.24493393103448274, 'lag_median': 0.211709}]}`
  lag_by_session_progress_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.3176470588235294], 'lag_mean': 0.2064123214285714, 'lag_median': 0.1640445}, {'bin': 'mid', 'n': 29, 'signal_range': [0.32941176470588235, 0.6588235294117647], 'lag_mean': 0.216578, 'lag_median': 0.186297}, {'bin': 'high', 'n': 29, 'signal_range': [0.6705882352941176, 1.0], 'lag_mean': 0.24493393103448274, 'lag_median': 0.211709}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2064123214285714, 'lag_median': 0.1640445}, {'bin': 'mid', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.216578, 'lag_median': 0.186297}, {'bin': 'high', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.24493393103448274, 'lag_median': 0.211709}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`
- https://www.perplexity.ai/|proxy
  response_size_bytes: `{'n': 86, 'mean': 9213.546511627907, 'median': 9222.0, 'min': 9179.0, 'max': 9243.0}`
  witness_depth60s: `{'n': 86, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [9179.0, 9200.0], 'lag_mean': 0.2549493571428571, 'lag_median': 0.24259999999999998}, {'bin': 'mid', 'n': 29, 'signal_range': [9200.0, 9222.0], 'lag_mean': 0.28227931034482756, 'lag_median': 0.221045}, {'bin': 'high', 'n': 29, 'signal_range': [9222.0, 9243.0], 'lag_mean': 0.40764862068965513, 'lag_median': 0.349555}]}`
  lag_by_depth60s_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.0], 'lag_mean': 0.23953635714285712, 'lag_median': 0.1969235}, {'bin': 'mid', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.3008965172413793, 'lag_median': 0.275534}, {'bin': 'high', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.4039129310344828, 'lag_median': 0.326539}]}`
  lag_by_session_progress_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.3176470588235294], 'lag_mean': 0.23953635714285712, 'lag_median': 0.1969235}, {'bin': 'mid', 'n': 29, 'signal_range': [0.32941176470588235, 0.6588235294117647], 'lag_mean': 0.3008965172413793, 'lag_median': 0.275534}, {'bin': 'high', 'n': 29, 'signal_range': [0.6705882352941176, 1.0], 'lag_mean': 0.4039129310344828, 'lag_median': 0.326539}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 86, 'bins': [{'bin': 'low', 'n': 28, 'signal_range': [0.0, 0.0], 'lag_mean': 0.23953635714285712, 'lag_median': 0.1969235}, {'bin': 'mid', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.3008965172413793, 'lag_median': 0.275534}, {'bin': 'high', 'n': 29, 'signal_range': [0.0, 0.0], 'lag_mean': 0.4039129310344828, 'lag_median': 0.326539}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`

## Notes
- `count_probe_gaps_over_threshold` flags potential reset/gap windows.
- `sector15_*` sections keep D15 compatibility in the federation lane.
- `lag_vs_phi/psi/sigma/epsilon` use nearest status snapshot per probe timestamp.

JSON: `reports_runtime/federation_dual_webapp_lag_gap_analysis_20260220T143106Z.json`
