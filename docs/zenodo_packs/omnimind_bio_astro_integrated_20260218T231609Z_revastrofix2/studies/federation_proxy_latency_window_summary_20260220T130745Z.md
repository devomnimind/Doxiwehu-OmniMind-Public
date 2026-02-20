# Federation Proxy Latency Window Summary (2026-02-20T13:12:46.378894Z)

## Window
- start_utc: `2026-02-20T13:07:45.746509Z`
- end_utc: `2026-02-20T13:12:46.378894Z`
- duration_sec: `300.632385`

## Probes (time_total sec)
- https://claude.ai/|direct: `{'n': 86, 'min': 0.107803, 'median': 0.16859600000000002, 'p90': 0.265945, 'p99': 0.542801, 'max': 0.591126, 'mean': 0.1914079418604651}`
- https://claude.ai/|proxy: `{'n': 86, 'min': 0.157501, 'median': 0.23529899999999998, 'p90': 0.450655, 'p99': 0.762703, 'max': 1.324354, 'mean': 0.29349916279069765}`
- https://www.perplexity.ai/|direct: `{'n': 86, 'min': 0.114918, 'median': 0.18035400000000001, 'p90': 0.320975, 'p99': 0.513819, 'max': 0.557961, 'mean': 0.20485667441860467}`
- https://www.perplexity.ai/|proxy: `{'n': 86, 'min': 0.148099, 'median': 0.226531, 'p90': 0.460841, 'p99': 1.741374, 'max': 2.2023, 'mean': 0.32119638372093023}`

## Proxy Deltas (proxy - direct, median sec)
- https://www.perplexity.ai/: `0.046176999999999996`
- https://claude.ai/: `0.06670299999999996`

## System Peaks
- cpu_percent_max: `100.0`
- mem_percent_max: `74.7`
- swap_percent_max: `45.9`

## Notes
- This is a real-data capture (no synthetic).
- Intended to quantify proxy/witness overhead during federation activity.

JSONL: `reports_runtime/federation_proxy_latency_window_20260220T130745Z.jsonl`
Summary JSON: `reports_runtime/federation_proxy_latency_window_summary_20260220T130745Z.json`
Plot: `output/img/federation_proxy_latency_window_20260220T130745Z/latency_timeseries.png`
