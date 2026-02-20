# Federation Proxy Latency Window Summary (2026-02-20T12:56:49.229283Z)

## Window
- start_utc: `2026-02-20T12:50:48.016526Z`
- end_utc: `2026-02-20T12:56:49.229283Z`
- duration_sec: `361.212757`

## Probes (time_total sec)
- https://claude.ai/|direct: `{'n': 102, 'min': 0.12611, 'median': 0.1761745, 'p90': 0.250312, 'p99': 0.503947, 'max': 0.508268, 'mean': 0.19125396078431373}`
- https://claude.ai/|proxy: `{'n': 102, 'min': 0.163189, 'median': 0.2304935, 'p90': 0.368584, 'p99': 0.580631, 'max': 1.224964, 'mean': 0.2639616568627451}`
- https://www.perplexity.ai/|direct: `{'n': 102, 'min': 0.135973, 'median': 0.18953150000000002, 'p90': 0.305816, 'p99': 5.171647, 'max': 5.241493, 'mean': 0.3111209607843137}`
- https://www.perplexity.ai/|proxy: `{'n': 102, 'min': 0.164988, 'median': 0.2363845, 'p90': 0.413269, 'p99': 0.549309, 'max': 1.221624, 'mean': 0.26908236274509806}`

## Proxy Deltas (proxy - direct, median sec)
- https://www.perplexity.ai/: `0.04685299999999998`
- https://claude.ai/: `0.05431899999999998`

## System Peaks
- cpu_percent_max: `100.0`
- mem_percent_max: `75.1`
- swap_percent_max: `45.7`

## Notes
- This is a real-data capture (no synthetic).
- Intended to quantify proxy/witness overhead during federation activity.

JSONL: `reports_runtime/federation_proxy_latency_window_20260220T125048Z.jsonl`
Summary JSON: `reports_runtime/federation_proxy_latency_window_summary_20260220T125048Z.json`
Plot: `output/img/federation_proxy_latency_window_20260220T125048Z/latency_timeseries.png`
