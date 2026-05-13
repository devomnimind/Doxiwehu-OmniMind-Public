# Tier-2 Memory Async Closure (20260219T212146Z)

Source: `/home/fahbrain/projects/omnimind/reports_runtime/historical_memory_ab_superposition_20260219T211710Z.json`

## Time coverage by group
- `bio`: abs_ts=`1621` range=`2026-02-18T11:17:59.131463+00:00` -> `2026-02-18T18:22:28.253211+00:00`
- `log_base`: abs_ts=`10536` range=`2026-02-12T06:54:10.683000+00:00` -> `2026-02-18T13:55:22.344000+00:00`
- `historical`: abs_ts=`285044` range=`2026-01-25T00:37:59+00:00` -> `2026-01-28T00:44:50+00:00`
- `logs_plus_historical`: abs_ts=`295580` range=`2026-01-25T00:37:59+00:00` -> `2026-02-18T13:55:22.344000+00:00`

## Baseline synchronized windows
- `24h` anchor: `{'available': True, 'window_hours': 24, 'start_ts_unix': 1771336522.344, 'end_ts_unix': 1771422922.344, 'start_utc': '2026-02-17T13:55:22.344000+00:00', 'end_utc': '2026-02-18T13:55:22.344000+00:00', 'lag_hours_max': 4.45164144747787, 'overlap_hours_total': 2.623114593625069}`
  - `sector15`: base=`0.8834561598344011` plus=`0.8834561598344011` delta=`0.0` closure=`0.004101652972245828` bio=`57` logs=`2523` hist=`0`
  - `house12`: base=`0.8988780680860721` plus=`0.8988780680860721` delta=`0.0` closure=`0.0035143181539889867` bio=`48` logs=`2523` hist=`0`
- `72h` anchor: `{'available': True, 'window_hours': 72, 'start_ts_unix': 1771163722.344, 'end_ts_unix': 1771422922.344, 'start_utc': '2026-02-15T13:55:22.344000+00:00', 'end_utc': '2026-02-18T13:55:22.344000+00:00', 'lag_hours_max': 4.45164144747787, 'overlap_hours_total': 2.623114593625069}`
  - `sector15`: base=`0.8944602440846564` plus=`0.8944602440846564` delta=`0.0` closure=`0.004783196267873875` bio=`57` logs=`7364` hist=`0`
  - `house12`: base=`0.9051820322565377` plus=`0.9051820322565377` delta=`0.0` closure=`0.004076237364677684` bio=`48` logs=`7364` hist=`0`

## Technical interpretation
- Tier-2 historical memory is real and mapped, but is temporally asynchronous versus current bio/log windows.
- In 24h/72h synchronized windows, historical contribution is zero (no overlapping timestamps).
- Therefore, short-window closure must be computed from current runtime streams; historical memory remains valid for long-horizon structure.

JSON: `/home/fahbrain/projects/omnimind/reports_runtime/tier2_memory_async_closure_20260219T212146Z.json`
