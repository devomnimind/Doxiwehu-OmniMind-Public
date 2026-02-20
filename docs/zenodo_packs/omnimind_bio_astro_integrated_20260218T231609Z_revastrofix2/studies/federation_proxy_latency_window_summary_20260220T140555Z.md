# Federation Proxy Latency Window Summary (2026-02-20T14:12:57.527528Z)

## Window
- start_utc: `2026-02-20T14:05:55.660093Z`
- end_utc: `2026-02-20T14:12:57.527528Z`
- duration_sec: `421.867435`

## Probes (time_total sec)
- https://claude.ai/|direct: `{'n': 126, 'min': 0.120742, 'median': 0.1655815, 'p90': 0.251197, 'p99': 0.506056, 'max': 0.600359, 'mean': 0.1909513095238095}`
- https://claude.ai/|proxy: `{'n': 126, 'min': 0.167049, 'median': 0.2205455, 'p90': 0.403696, 'p99': 2.466054, 'max': 2.492446, 'mean': 0.31809332539682544}`
- https://www.perplexity.ai/|direct: `{'n': 126, 'min': 0.131071, 'median': 0.17325200000000002, 'p90': 0.292405, 'p99': 0.498941, 'max': 0.619705, 'mean': 0.20038057936507936}`
- https://www.perplexity.ai/|proxy: `{'n': 126, 'min': 0.154126, 'median': 0.22121600000000002, 'p90': 0.394995, 'p99': 1.271382, 'max': 1.456025, 'mean': 0.2785248888888889}`

## Proxy Deltas (proxy - direct, median sec)
- https://claude.ai/: `0.05496400000000001`
- https://www.perplexity.ai/: `0.04796400000000001`

## System Peaks
- cpu_percent_max: `100.0`
- mem_percent_max: `77.5`
- swap_percent_max: `45.9`

## Notes
- This is a real-data capture (no synthetic).
- Intended to quantify proxy/witness overhead during federation activity.

JSONL: `reports_runtime/federation_proxy_latency_window_20260220T140555Z.jsonl`
Summary JSON: `reports_runtime/federation_proxy_latency_window_summary_20260220T140555Z.json`
Plot: `output/img/federation_proxy_latency_window_20260220T140555Z/latency_timeseries.png`
