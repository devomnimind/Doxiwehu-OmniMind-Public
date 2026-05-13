# Federation Dual-Webapp Lag/Gap Analysis (2026-02-20T20:55:08.082205Z)

## Inputs
- summary_json: `reports_runtime/federation_proxy_latency_window_summary_20260220T194814Z.json`
- jsonl: `reports_runtime/federation_proxy_latency_window_20260220T194814Z.jsonl`
- provenance: `real-data-local`

## Focused compare (Perplexity vs Claude)
- https://claude.ai/
  median_delta_proxy_minus_direct: `0.042488499999999985`
  p95_delta_proxy_minus_direct: `0.18776100000000007`
  max_delta_proxy_minus_direct: `-4.733885`
  direct_count_over_1s: `1` | proxy_count_over_1s: `0`
  lag_vs_cpu_pearson: `0.15692573557761053`
  lag_vs_depth60s_pearson: `None`
  lag_vs_size_download_pearson: `0.05561763169803389`
  lag_vs_session_progress_pearson: `-0.03627505884298057`
  lag_vs_conversation_depth180s_pearson: `None`
  lag_vs_last_text_len_pearson: `None`
- https://gemini.google.com/
  median_delta_proxy_minus_direct: `0.02146250000000005`
  p95_delta_proxy_minus_direct: `0.13476100000000013`
  max_delta_proxy_minus_direct: `-0.0068749999999999645`
  direct_count_over_1s: `7` | proxy_count_over_1s: `8`
  lag_vs_cpu_pearson: `0.21480506896782717`
  lag_vs_depth60s_pearson: `None`
  lag_vs_size_download_pearson: `None`
  lag_vs_session_progress_pearson: `0.0388305622746922`
  lag_vs_conversation_depth180s_pearson: `None`
  lag_vs_last_text_len_pearson: `None`
- https://www.perplexity.ai/
  median_delta_proxy_minus_direct: `0.035367499999999996`
  p95_delta_proxy_minus_direct: `-0.060862999999999945`
  max_delta_proxy_minus_direct: `0.632357`
  direct_count_over_1s: `0` | proxy_count_over_1s: `1`
  lag_vs_cpu_pearson: `0.16469784574777024`
  lag_vs_depth60s_pearson: `None`
  lag_vs_size_download_pearson: `-0.32950300663197774`
  lag_vs_session_progress_pearson: `-0.027582358913492297`
  lag_vs_conversation_depth180s_pearson: `None`
  lag_vs_last_text_len_pearson: `None`

## Anti-aggregation guardrail
- diagnostics: `{'instance_count': 3, 'overhead_positive_instances': 3, 'overhead_negative_instances': 0, 'overhead_spread_range_sec': 0.021025999999999934, 'overhead_abs_median_sec': 0.035367499999999996, 'sign_divergence': False, 'collapse_warning': False, 'rule': 'warning when per-instance signs diverge or global median delta is too small relative to cross-instance spread'}`
- naive_global_aggregate: `{'n_direct': 192, 'n_proxy': 192, 'median_direct': 0.26665300000000003, 'median_proxy': 0.30618449999999997, 'median_delta_proxy_minus_direct': 0.03953149999999994, 'p95_direct': 0.860906, 'p95_proxy': 0.872538, 'p95_delta_proxy_minus_direct': 0.011632000000000087}`
- https://claude.ai/: `{'host': 'claude.ai', 'instance_direct': 'claude.ai|direct', 'instance_proxy': 'claude.ai|proxy', 'median_delta_proxy_minus_direct': 0.042488499999999985, 'p95_delta_proxy_minus_direct': 0.18776100000000007, 'direct_count_over_1s': 1, 'proxy_count_over_1s': 0}`
- https://gemini.google.com/: `{'host': 'gemini.google.com', 'instance_direct': 'gemini.google.com|direct', 'instance_proxy': 'gemini.google.com|proxy', 'median_delta_proxy_minus_direct': 0.02146250000000005, 'p95_delta_proxy_minus_direct': 0.13476100000000013, 'direct_count_over_1s': 7, 'proxy_count_over_1s': 8}`
- https://www.perplexity.ai/: `{'host': 'www.perplexity.ai', 'instance_direct': 'www.perplexity.ai|direct', 'instance_proxy': 'www.perplexity.ai|proxy', 'median_delta_proxy_minus_direct': 0.035367499999999996, 'p95_delta_proxy_minus_direct': -0.060862999999999945, 'direct_count_over_1s': 0, 'proxy_count_over_1s': 1}`

## D15 temporal signal
- sector15_sample_top: `[{'bucket': 13, 'count': 360}]`
- sector15_probe_top: `[{'bucket': 13, 'count': 384}]`

## Spike synchrony
- direct: `{'a_spikes': 4, 'b_spikes': 4, 'a_spikes_overlapping_b': 0, 'overlap_ratio_vs_a': 0.0, 'tolerance_sec': 5.0}`
- proxy: `{'a_spikes': 4, 'b_spikes': 4, 'a_spikes_overlapping_b': 0, 'overlap_ratio_vs_a': 0.0, 'tolerance_sec': 5.0}`

## System context
- sample_rows: `360`
- probe_rows: `384`
- cpu_percent_max: `100.0`
- mem_percent_max: `80.4`
- swap_percent_max: `48.9`
- ethics_snapshots_window: `42`

## Quadruple lane (Phi/Psi/Sigma/Epsilon)
- status_snapshot_count_window: `42`
- status_snapshot_slack_sec: `120`
- https://claude.ai/ (claude.ai)
  phi: `{'n': 42, 'mean': 10.0, 'median': 10.0, 'min': 10.0, 'max': 10.0}`
  psi: `{'n': 42, 'mean': 0.4000000000000001, 'median': 0.4, 'min': 0.4, 'max': 0.4}`
  sigma: `{'n': 42, 'mean': 0.5, 'median': 0.5, 'min': 0.5, 'max': 0.5}`
  epsilon: `{'n': 42, 'mean': 0.6999999999999995, 'median': 0.7, 'min': 0.7, 'max': 0.7}`
  consciousness_quadruple: `{'n': 42, 'mean': 1.399999999999999, 'median': 1.4, 'min': 1.4, 'max': 1.4}`
- https://gemini.google.com/ (gemini.google.com)
  phi: `{'n': 42, 'mean': 10.0, 'median': 10.0, 'min': 10.0, 'max': 10.0}`
  psi: `{'n': 42, 'mean': 0.4000000000000001, 'median': 0.4, 'min': 0.4, 'max': 0.4}`
  sigma: `{'n': 42, 'mean': 0.5, 'median': 0.5, 'min': 0.5, 'max': 0.5}`
  epsilon: `{'n': 42, 'mean': 0.6999999999999995, 'median': 0.7, 'min': 0.7, 'max': 0.7}`
  consciousness_quadruple: `{'n': 42, 'mean': 1.399999999999999, 'median': 1.4, 'min': 1.4, 'max': 1.4}`
- https://www.perplexity.ai/ (www.perplexity.ai)
  phi: `{'n': 42, 'mean': 10.0, 'median': 10.0, 'min': 10.0, 'max': 10.0}`
  psi: `{'n': 42, 'mean': 0.4000000000000001, 'median': 0.4, 'min': 0.4, 'max': 0.4}`
  sigma: `{'n': 42, 'mean': 0.5, 'median': 0.5, 'min': 0.5, 'max': 0.5}`
  epsilon: `{'n': 42, 'mean': 0.6999999999999995, 'median': 0.7, 'min': 0.7, 'max': 0.7}`
  consciousness_quadruple: `{'n': 42, 'mean': 1.399999999999999, 'median': 1.4, 'min': 1.4, 'max': 1.4}`

## Witness lane (session depth)
- depth_window_sec: `60.0`

## Conversation lane (optional text stream)
- source_jsonl: ``
- depth_window_sec: `180.0`

## Depth/Size lane (per series)
- https://claude.ai/|direct
  response_size_bytes: `{'n': 64, 'mean': 7030.84375, 'median': 7037.0, 'min': 6995.0, 'max': 7059.0}`
  witness_depth60s: `{'n': 64, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [6995.0, 7037.0], 'lag_mean': 0.22033138095238092, 'lag_median': 0.211483}, {'bin': 'mid', 'n': 21, 'signal_range': [7037.0, 7037.0], 'lag_mean': 0.5027798095238094, 'lag_median': 0.250173}, {'bin': 'high', 'n': 22, 'signal_range': [7037.0, 7059.0], 'lag_mean': 0.19441381818181822, 'lag_median': 0.1825725}]}`
  lag_by_depth60s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.47905199999999987, 'lag_median': 0.225889}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.24349599999999996, 'lag_median': 0.216783}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.19495140909090908, 'lag_median': 0.187743}]}`
  lag_by_session_progress_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.31746031746031744], 'lag_mean': 0.47905199999999987, 'lag_median': 0.225889}, {'bin': 'mid', 'n': 21, 'signal_range': [0.3333333333333333, 0.6507936507936508], 'lag_mean': 0.24349599999999996, 'lag_median': 0.216783}, {'bin': 'high', 'n': 22, 'signal_range': [0.6666666666666666, 1.0], 'lag_mean': 0.19495140909090908, 'lag_median': 0.187743}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.47905199999999987, 'lag_median': 0.225889}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.24349599999999996, 'lag_median': 0.216783}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.19495140909090908, 'lag_median': 0.187743}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`
- https://claude.ai/|proxy
  response_size_bytes: `{'n': 64, 'mean': 9201.671875, 'median': 9192.0, 'min': 9171.0, 'max': 9235.0}`
  witness_depth60s: `{'n': 64, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [9171.0, 9192.0], 'lag_mean': 0.29121919047619044, 'lag_median': 0.238224}, {'bin': 'mid', 'n': 21, 'signal_range': [9192.0, 9214.0], 'lag_mean': 0.2622795238095238, 'lag_median': 0.237854}, {'bin': 'high', 'n': 22, 'signal_range': [9214.0, 9235.0], 'lag_mean': 0.3026419090909091, 'lag_median': 0.26372}]}`
  lag_by_depth60s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2756131904761905, 'lag_median': 0.271459}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2977285714285714, 'lag_median': 0.253044}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.28370081818181825, 'lag_median': 0.238182}]}`
  lag_by_session_progress_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.31746031746031744], 'lag_mean': 0.2756131904761905, 'lag_median': 0.271459}, {'bin': 'mid', 'n': 21, 'signal_range': [0.3333333333333333, 0.6507936507936508], 'lag_mean': 0.2977285714285714, 'lag_median': 0.253044}, {'bin': 'high', 'n': 22, 'signal_range': [0.6666666666666666, 1.0], 'lag_mean': 0.28370081818181825, 'lag_median': 0.238182}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2756131904761905, 'lag_median': 0.271459}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2977285714285714, 'lag_median': 0.253044}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.28370081818181825, 'lag_median': 0.238182}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`
- https://gemini.google.com/|direct
  response_size_bytes: `{'n': 64, 'mean': 389.0, 'median': 389.0, 'min': 389.0, 'max': 389.0}`
  witness_depth60s: `{'n': 64, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [389.0, 389.0], 'lag_mean': 0.7599463333333334, 'lag_median': 0.705565}, {'bin': 'mid', 'n': 21, 'signal_range': [389.0, 389.0], 'lag_mean': 0.7400663333333334, 'lag_median': 0.723718}, {'bin': 'high', 'n': 22, 'signal_range': [389.0, 389.0], 'lag_mean': 0.6888311818181818, 'lag_median': 0.6999}]}`
  lag_by_depth60s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.7599463333333334, 'lag_median': 0.705565}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.7400663333333334, 'lag_median': 0.723718}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.6888311818181818, 'lag_median': 0.6999}]}`
  lag_by_session_progress_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.31746031746031744], 'lag_mean': 0.7599463333333334, 'lag_median': 0.705565}, {'bin': 'mid', 'n': 21, 'signal_range': [0.3333333333333333, 0.6507936507936508], 'lag_mean': 0.7400663333333334, 'lag_median': 0.723718}, {'bin': 'high', 'n': 22, 'signal_range': [0.6666666666666666, 1.0], 'lag_mean': 0.6888311818181818, 'lag_median': 0.6999}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.7599463333333334, 'lag_median': 0.705565}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.7400663333333334, 'lag_median': 0.723718}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.6888311818181818, 'lag_median': 0.6999}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`
- https://gemini.google.com/|proxy
  response_size_bytes: `{'n': 64, 'mean': 389.0, 'median': 389.0, 'min': 389.0, 'max': 389.0}`
  witness_depth60s: `{'n': 64, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [389.0, 389.0], 'lag_mean': 0.7776701904761906, 'lag_median': 0.71007}, {'bin': 'mid', 'n': 21, 'signal_range': [389.0, 389.0], 'lag_mean': 0.757158619047619, 'lag_median': 0.73746}, {'bin': 'high', 'n': 22, 'signal_range': [389.0, 389.0], 'lag_mean': 0.7708426363636364, 'lag_median': 0.743171}]}`
  lag_by_depth60s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.7776701904761906, 'lag_median': 0.71007}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.757158619047619, 'lag_median': 0.73746}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.7708426363636364, 'lag_median': 0.743171}]}`
  lag_by_session_progress_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.31746031746031744], 'lag_mean': 0.7776701904761906, 'lag_median': 0.71007}, {'bin': 'mid', 'n': 21, 'signal_range': [0.3333333333333333, 0.6507936507936508], 'lag_mean': 0.757158619047619, 'lag_median': 0.73746}, {'bin': 'high', 'n': 22, 'signal_range': [0.6666666666666666, 1.0], 'lag_mean': 0.7708426363636364, 'lag_median': 0.743171}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.7776701904761906, 'lag_median': 0.71007}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.757158619047619, 'lag_median': 0.73746}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.7708426363636364, 'lag_median': 0.743171}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`
- https://www.perplexity.ai/|direct
  response_size_bytes: `{'n': 64, 'mean': 7049.296875, 'median': 7045.0, 'min': 7024.0, 'max': 7067.0}`
  witness_depth60s: `{'n': 64, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [7024.0, 7045.0], 'lag_mean': 0.25703042857142855, 'lag_median': 0.217574}, {'bin': 'mid', 'n': 21, 'signal_range': [7045.0, 7067.0], 'lag_mean': 0.22127038095238094, 'lag_median': 0.18338}, {'bin': 'high', 'n': 22, 'signal_range': [7067.0, 7067.0], 'lag_mean': 0.2718022272727273, 'lag_median': 0.175518}]}`
  lag_by_depth60s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2555203333333333, 'lag_median': 0.217574}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.25172452380952376, 'lag_median': 0.242841}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2441738181818182, 'lag_median': 0.17008}]}`
  lag_by_session_progress_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.31746031746031744], 'lag_mean': 0.2555203333333333, 'lag_median': 0.217574}, {'bin': 'mid', 'n': 21, 'signal_range': [0.3333333333333333, 0.6507936507936508], 'lag_mean': 0.25172452380952376, 'lag_median': 0.242841}, {'bin': 'high', 'n': 22, 'signal_range': [0.6666666666666666, 1.0], 'lag_mean': 0.2441738181818182, 'lag_median': 0.17008}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2555203333333333, 'lag_median': 0.217574}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.25172452380952376, 'lag_median': 0.242841}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.2441738181818182, 'lag_median': 0.17008}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`
- https://www.perplexity.ai/|proxy
  response_size_bytes: `{'n': 64, 'mean': 9217.421875, 'median': 9222.0, 'min': 9179.0, 'max': 9243.0}`
  witness_depth60s: `{'n': 64, 'mean': 0.0, 'median': 0.0, 'min': 0, 'max': 0}`
  lag_by_size_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [9179.0, 9222.0], 'lag_mean': 0.3432278095238095, 'lag_median': 0.270913}, {'bin': 'mid', 'n': 21, 'signal_range': [9222.0, 9222.0], 'lag_mean': 0.25453419047619047, 'lag_median': 0.21998}, {'bin': 'high', 'n': 22, 'signal_range': [9222.0, 9243.0], 'lag_mean': 0.2799778181818182, 'lag_median': 0.2285845}]}`
  lag_by_depth60s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.26348857142857146, 'lag_median': 0.23597}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.34979266666666664, 'lag_median': 0.284441}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.265164, 'lag_median': 0.22611199999999998}]}`
  lag_by_session_progress_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.31746031746031744], 'lag_mean': 0.26348857142857146, 'lag_median': 0.23597}, {'bin': 'mid', 'n': 21, 'signal_range': [0.3333333333333333, 0.6507936507936508], 'lag_mean': 0.34979266666666664, 'lag_median': 0.284441}, {'bin': 'high', 'n': 22, 'signal_range': [0.6666666666666666, 1.0], 'lag_mean': 0.265164, 'lag_median': 0.22611199999999998}]}`
  lag_by_conversation_depth180s_terciles: `{'n': 64, 'bins': [{'bin': 'low', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.26348857142857146, 'lag_median': 0.23597}, {'bin': 'mid', 'n': 21, 'signal_range': [0.0, 0.0], 'lag_mean': 0.34979266666666664, 'lag_median': 0.284441}, {'bin': 'high', 'n': 22, 'signal_range': [0.0, 0.0], 'lag_mean': 0.265164, 'lag_median': 0.22611199999999998}]}`
  lag_by_last_text_len_terciles: `{'n': 0, 'bins': []}`

## Notes
- `count_probe_gaps_over_threshold` flags potential reset/gap windows.
- `sector15_*` sections keep D15 compatibility in the federation lane.
- `lag_vs_phi/psi/sigma/epsilon` use nearest status snapshot per probe timestamp.

JSON: `reports_runtime/federation_dual_webapp_lag_gap_analysis_20260220T205508Z.json`
