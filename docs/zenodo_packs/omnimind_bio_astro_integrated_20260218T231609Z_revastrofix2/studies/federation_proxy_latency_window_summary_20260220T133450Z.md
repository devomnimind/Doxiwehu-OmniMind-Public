# Federation Proxy Latency Window Summary (2026-02-20T13:39:53.918901Z)

## Window
- start_utc: `2026-02-20T13:34:50.480739Z`
- end_utc: `2026-02-20T13:39:53.918901Z`
- duration_sec: `303.438162`

## Probes (time_total sec)
- https://claude.ai/|direct: `{'n': 87, 'min': 0.11924, 'median': 0.17895, 'p90': 0.261277, 'p99': 0.466884, 'max': 0.564711, 'mean': 0.19656458620689657}`
- https://claude.ai/|proxy: `{'n': 87, 'min': 0.162831, 'median': 0.287494, 'p90': 0.495265, 'p99': 1.289484, 'max': 1.419577, 'mean': 0.33828432183908047}`
- https://www.perplexity.ai/|direct: `{'n': 87, 'min': 0.108296, 'median': 0.170333, 'p90': 0.414978, 'p99': 0.629228, 'max': 0.925885, 'mean': 0.22096416091954021}`
- https://www.perplexity.ai/|proxy: `{'n': 87, 'min': 0.168807, 'median': 0.28033, 'p90': 0.458793, 'p99': 1.388837, 'max': 1.629414, 'mean': 0.3418295172413793}`

## Proxy Deltas (proxy - direct, median sec)
- https://claude.ai/: `0.10854400000000003`
- https://www.perplexity.ai/: `0.10999700000000001`

## System Peaks
- cpu_percent_max: `100.0`
- mem_percent_max: `75.7`
- swap_percent_max: `45.8`

## Notes
- This is a real-data capture (no synthetic).
- Intended to quantify proxy/witness overhead during federation activity.

JSONL: `reports_runtime/federation_proxy_latency_window_20260220T133450Z.jsonl`
Summary JSON: `reports_runtime/federation_proxy_latency_window_summary_20260220T133450Z.json`
Plot: `output/img/federation_proxy_latency_window_20260220T133450Z/latency_timeseries.png`
