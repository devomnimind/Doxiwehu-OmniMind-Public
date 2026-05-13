# Federation Proxy Latency Window Summary (2026-02-20T14:30:56.405694Z)

## Window
- start_utc: `2026-02-20T14:25:53.787895Z`
- end_utc: `2026-02-20T14:30:56.405694Z`
- duration_sec: `302.617799`

## Probes (time_total sec)
- https://claude.ai/|direct: `{'n': 86, 'min': 0.133883, 'median': 0.1960755, 'p90': 0.339897, 'p99': 0.491371, 'max': 0.580838, 'mean': 0.22475987209302326}`
- https://claude.ai/|proxy: `{'n': 86, 'min': 0.156741, 'median': 0.270379, 'p90': 0.513272, 'p99': 1.050413, 'max': 1.361212, 'mean': 0.33298438372093025}`
- https://www.perplexity.ai/|direct: `{'n': 86, 'min': 0.126599, 'median': 0.182747, 'p90': 0.313436, 'p99': 0.622951, 'max': 0.832719, 'mean': 0.22283012790697676}`
- https://www.perplexity.ai/|proxy: `{'n': 86, 'min': 0.148359, 'median': 0.2592595, 'p90': 0.463313, 'p99': 1.047681, 'max': 1.855823, 'mean': 0.3156568837209302}`

## Proxy Deltas (proxy - direct, median sec)
- https://claude.ai/: `0.07430349999999997`
- https://www.perplexity.ai/: `0.07651249999999998`

## System Peaks
- cpu_percent_max: `100.0`
- mem_percent_max: `79.3`
- swap_percent_max: `46.4`

## Notes
- This is a real-data capture (no synthetic).
- Intended to quantify proxy/witness overhead during federation activity.

JSONL: `reports_runtime/federation_proxy_latency_window_20260220T142553Z.jsonl`
Summary JSON: `reports_runtime/federation_proxy_latency_window_summary_20260220T142553Z.json`
Plot: `output/img/federation_proxy_latency_window_20260220T142553Z/latency_timeseries.png`
