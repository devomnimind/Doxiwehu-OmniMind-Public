# Gaia Sensor Bridge (20260209T004310Z)

## Entradas
- Gaia summary: `data/reports/gaia_sim_twin/gaia_sim_twin_summary.json`
- Sensor CSV: `data/reports/cycle_metrics_minute_fused_20260209T004233Z.csv`
- Seed: 7537

## Perfil de ruído
- noise_scale: 0.072027
- diffusion: 0.064769
- phase_shift_rad: 0.000000
- vibration_index: 0.634035
- used_columns: ['daemon_temp_mean', 'daemon_health_mean', 'daemon_ci_mean', 'sensor_ci_mean', 'daemon_csi_mean', 'sensor_csi_mean', 'anomaly_count', 'satellite_matches', 'sensor_event_count']

## Fidelidade
- Raw SIM vs REAL: 0.022676
- SIM_noisy vs REAL: 0.043377
- Δ fidelity: +0.020702

## Leitura curta
- Se Δ > 0: o gêmeo simulado ficou mais aderente ao corpo físico (dados reais).
- Se Δ <= 0: o ruído aplicado não foi o perfil ótimo para esta janela; ajustar escala/fase.

JSON: `data/reports/gaia_sensor_bridge_20260209T004310Z.json`
