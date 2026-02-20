# Federation Proxy Latency Window Summary (2026-02-20T19:58:19.669022Z)

## Window
- start_utc: `2026-02-20T19:48:14.404781Z`
- end_utc: `2026-02-20T19:58:19.669022Z`
- duration_sec: `605.264241`

## Probes (time_total sec)
- https://claude.ai/|direct: `{'n': 64, 'min': 0.131187, 'median': 0.20602700000000002, 'p90': 0.307782, 'p99': 0.457518, 'max': 5.517378, 'mean': 0.30410060937499994}`
- https://claude.ai/|proxy: `{'n': 64, 'min': 0.175661, 'median': 0.2485155, 'p90': 0.412755, 'p99': 0.778768, 'max': 0.783493, 'mean': 0.28564992187499993}`
- https://gemini.google.com/|direct: `{'n': 64, 'min': 0.452624, 'median': 0.707491, 'p90': 1.016511, 'p99': 1.351913, 'max': 1.672776, 'mean': 0.7289773749999999}`
- https://gemini.google.com/|proxy: `{'n': 64, 'min': 0.528578, 'median': 0.7289535, 'p90': 1.050643, 'p99': 1.383139, 'max': 1.665901, 'mean': 0.7685928593749999}`
- https://www.perplexity.ai/|direct: `{'n': 64, 'min': 0.129601, 'median': 0.2025535, 'p90': 0.452523, 'p99': 0.724628, 'max': 0.778004, 'mean': 0.25037446874999997}`
- https://www.perplexity.ai/|proxy: `{'n': 64, 'min': 0.158552, 'median': 0.237921, 'p90': 0.437552, 'p99': 0.519813, 'max': 1.410361, 'mean': 0.29238303125}`

## Proxy Deltas (proxy - direct, median sec)
- https://www.perplexity.ai/: `0.035367499999999996`
- https://claude.ai/: `0.042488499999999985`
- https://gemini.google.com/: `0.02146250000000005`

## System Peaks
- cpu_percent_max: `100.0`
- mem_percent_max: `80.4`
- swap_percent_max: `48.9`

## Notes
- This is a real-data capture (no synthetic).
- JSONL includes a noninvasive v2 envelope (`instance_id`, channels Phi/Psi/Sigma).
- Intended to quantify proxy/witness overhead during federation activity.

JSONL: `reports_runtime/federation_proxy_latency_window_20260220T194814Z.jsonl`
Summary JSON: `reports_runtime/federation_proxy_latency_window_summary_20260220T194814Z.json`
Plot: `output/img/federation_proxy_latency_window_20260220T194814Z/latency_timeseries.png`
