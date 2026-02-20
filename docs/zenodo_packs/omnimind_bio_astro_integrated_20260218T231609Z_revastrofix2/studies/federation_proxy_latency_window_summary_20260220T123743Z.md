# Federation Proxy Latency Window Summary (2026-02-20T12:42:44.361380Z)

## Window
- start_utc: `2026-02-20T12:37:43.343859Z`
- end_utc: `2026-02-20T12:42:44.361380Z`
- duration_sec: `301.017521`

## Probes (time_total sec)
- https://github.com/|direct: `{'n': 30, 'min': 0.2348, 'median': 0.3355095, 'p90': 0.494078, 'p99': 0.657339, 'max': 0.657339, 'mean': 0.360459}`
- https://github.com/|proxy: `{'n': 30, 'min': 0.269166, 'median': 0.36647399999999997, 'p90': 0.487667, 'p99': 0.809954, 'max': 0.809954, 'mean': 0.3940554666666667}`
- https://www.perplexity.ai/|direct: `{'n': 30, 'min': 0.131781, 'median': 0.1827585, 'p90': 0.2333, 'p99': 0.282454, 'max': 0.282454, 'mean': 0.18520356666666665}`
- https://www.perplexity.ai/|proxy: `{'n': 30, 'min': 0.17016, 'median': 0.23337750000000002, 'p90': 0.41748, 'p99': 2.278997, 'max': 2.278997, 'mean': 0.34780953333333336}`
- https://zenodo.org/|direct: `{'n': 30, 'min': 1.181349, 'median': 1.373743, 'p90': 1.484683, 'p99': 2.02203, 'max': 2.02203, 'mean': 1.3750781666666667}`
- https://zenodo.org/|proxy: `{'n': 30, 'min': 1.246445, 'median': 1.4690495000000001, 'p90': 1.718244, 'p99': 2.160242, 'max': 2.160242, 'mean': 1.5125248}`

## Proxy Deltas (proxy - direct, median sec)
- https://www.perplexity.ai/: `0.050619000000000025`
- https://zenodo.org/: `0.09530650000000018`
- https://github.com/: `0.03096449999999995`

## System Peaks
- cpu_percent_max: `99.9`
- mem_percent_max: `74.1`
- swap_percent_max: `45.6`

## Notes
- This is a real-data capture (no synthetic).
- Intended to quantify proxy/witness overhead during federation activity.

JSONL: `reports_runtime/federation_proxy_latency_window_20260220T123743Z.jsonl`
Summary JSON: `reports_runtime/federation_proxy_latency_window_summary_20260220T123743Z.json`
Plot: `output/img/federation_proxy_latency_window_20260220T123743Z/latency_timeseries.png`
