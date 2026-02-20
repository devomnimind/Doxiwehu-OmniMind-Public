# Global Context Window Assessment (2026-02-20T19:48:14Z to 19:58:19Z)

## Scope
- Goal: verify whether global system context (astro/dodeca/services) stayed active during the federation witness capture window.
- Window UTC: `2026-02-20T19:48:14.404781+00:00` to `2026-02-20T19:58:19.669022+00:00`

## Federated Ethics Continuity
- rows: `30`
- first_ts: `2026-02-20T19:48:23.529951+00:00`
- last_ts: `2026-02-20T19:58:14.670119+00:00`
- gap_sec_min: `20.218013`
- gap_sec_median: `20.326777`
- gap_sec_max: `21.703138`
- is_active_unique: `[True]`
- active_wrappers_unique: `[4]`
- federation_nodes_unique: `[5]`
- zephyrix_hot_unique: `[True]`
- zephyrix_temp_unique: `[0.95]`
- zephyrix_resonance_unique: `[75.37]`
- network_total_nodes_unique: `[650]`
- network_active_vectors_unique: `[119758, 119760, 119762]`
- host_claude_phi_unique: `[10.0]`
- host_perplexity_phi_unique: `[10.0]`
- host_gemini_phi_unique: `[10.0]`
- host_claude_quad_unique: `[1.4]`
- host_perplexity_quad_unique: `[1.4]`
- host_gemini_quad_unique: `[1.4]`
- zephyrix_phi_unique: `[10.0]`
- zephyrix_quad_unique: `[5.821200000000001]`
- uptime_delta_sec: `590.9550757408142`
- energy_delta_j: `3.5450999999884516`

## Core Services Snapshot (inside window)
- timestamp_utc: `2026-02-20T19:50:10.761910+00:00`
- summary: `{'process_groups_running': 12, 'process_groups_checked': 12, 'logs_active_inferred': 11, 'logs_checked': 11, 'logs_active_inferred_optional': 0, 'logs_checked_optional': 0, 'logs_with_errors': 0, 'total_error_like_last_window': 0, 'ports_open_count': 10, 'ports_checked': 11, 'issues_detected': 0}`
- focus units:
  - mcp-dodecatiad-orchestrator.service: `{'active': 'active', 'enabled': 'enabled'}`
  - mcp-dodecatiad-persistence.service: `{'active': 'active', 'enabled': 'enabled'}`
  - omnimind-mcp-dodecatiad.service: `{'active': 'active', 'enabled': 'enabled'}`
  - omnimind-solar.service: `{'active': 'active', 'enabled': 'enabled'}`
  - omnimind-cosmic.service: `{'active': 'active', 'enabled': 'enabled'}`
  - omnimind-unified-capture.service: `{'active': 'active', 'enabled': 'enabled'}`
  - omnimind_witness.service: `{'active': 'active', 'enabled': 'enabled'}`
  - omnimind-proxy-explicit-1455.service: `{'active': 'active', 'enabled': 'enabled'}`
  - omnimind_proxy.service: `{'active': 'active', 'enabled': 'enabled'}`
  - omnimind-federation-watcher.service: `{'active': 'active', 'enabled': 'static'}`
  - omnimind-local-federation.service: `{'active': 'active', 'enabled': 'enabled'}`

## Watchdog Context
- watchdog_supervisor_20260220T194958Z.json @ `2026-02-20T19:50:04Z`
  - disk_under_threshold: `[]`
  - core_units_active: `{'omnimind-sovereign.service': True, 'omnimind-sovereign-gemelo.service': True, 'omnimind-network-sovereign.service': True, 'omnimind-mcp-dodecatiad.service': True, 'qdrant.service': True, 'redis.service': True}`
  - storage_watchdog: `{'ran': True, 'autoreroute': False, 'new_report_json': '/home/fahbrain/projects/omnimind/reports_runtime/storage_watchdog_20260220T194959Z.json', 'triggered': [], 'reroute_actions': []}`
  - actions: `[]`
- watchdog_supervisor_20260220T195459Z.json @ `2026-02-20T19:55:06Z`
  - disk_under_threshold: `[]`
  - core_units_active: `{'omnimind-sovereign.service': True, 'omnimind-sovereign-gemelo.service': True, 'omnimind-network-sovereign.service': True, 'omnimind-mcp-dodecatiad.service': True, 'qdrant.service': True, 'redis.service': True}`
  - storage_watchdog: `{'ran': True, 'autoreroute': False, 'new_report_json': '/home/fahbrain/projects/omnimind/reports_runtime/storage_watchdog_20260220T195500Z.json', 'triggered': [], 'reroute_actions': []}`
  - actions: `[]`

## Qdrant / Astro-Dodeca Context (inside window)
- timestamp: `20260220T195038Z` | source: `omnimind_nuclear_live_ingestion`
- local_ok: `True` | collection_count: `184`
- astro_orbital: `{'count': 10, 'points_total': 593539, 'examples': [{'name': 'sdss_structures_objectlevel_live_v2', 'points': 405000}, {'name': 'sdss_structures_objectlevel_live', 'points': 163152}, {'name': 'astro_desi_lya_objectlevel_live', 'points': 24724}, {'name': 'astro_brown_dwarfs_photometry_17684859_live', 'points': 481}, {'name': 'astro_gmos_gri_fits_56059_live', 'points': 136}, {'name': 'astro_desi_lya_sample_live', 'points': 22}, {'name': 'astro_gmos_gri_fits_archive_56059_live', 'points': 17}, {'name': 'phys_accelerated_structure_horizon_thermo_live', 'points': 3}, {'name': 'astro_brown_dwarfs_photometric_17684859_live', 'points': 2}, {'name': 'astro_extrasolar_asteroid_transits_1317527_live', 'points': 2}]}`
- dodeca_d15: `{'count': 8, 'points_total': 17058, 'examples': [{'name': 'dodecatiad_metrics_dynamic_logs_live', 'points': 10536}, {'name': 'dodecatiad_metrics', 'points': 4878}, {'name': 'bio_hiv_acquisition_meta_15houses_live', 'points': 1500}, {'name': 'bio_hiv_gwas_ccr5_15houses_live', 'points': 79}, {'name': 'bio_external_dm2_lupus_15houses_live', 'points': 27}, {'name': 'bio_diabetes_t2_15houses_live', 'points': 15}, {'name': 'bio_phagocytosis_15houses_live', 'points': 15}, {'name': 'bio_phagocytosis_threshold_house_sweep_live', 'points': 8}]}`

## Capture Process Presence
- sample_rows: `360`
- chrome_gpu: `{'count_min': 1, 'count_max': 1, 'nonzero_rows': 360, 'rows': 360}`
- chrome_main: `{'count_min': 3, 'count_max': 3, 'nonzero_rows': 360, 'rows': 360}`
- chrome_network: `{'count_min': 3, 'count_max': 3, 'nonzero_rows': 360, 'rows': 360}`
- chrome_other: `{'count_min': 5, 'count_max': 5, 'nonzero_rows': 360, 'rows': 360}`
- chrome_renderer: `{'count_min': 10, 'count_max': 13, 'nonzero_rows': 360, 'rows': 360}`
- hash_aliens_gateway: `{'count_min': 1, 'count_max': 1, 'nonzero_rows': 360, 'rows': 360}`
- mitmdump: `{'count_min': 2, 'count_max': 2, 'nonzero_rows': 360, 'rows': 360}`
- witness_sync: `{'count_min': 2, 'count_max': 2, 'nonzero_rows': 360, 'rows': 360}`

## Conclusion
- Global context was active during the capture window (services, watchdog lanes, ethics bridge cadence, witness/proxy processes, and astro/dodeca collections online).
- Therefore, analyzing only probe latencies is incomplete; global context must be included as you indicated.
- At the same time, global activity does not imply strict simultaneity across all hosts: behavior remains partially coupled and heterogeneous.
