# Trajectory Fidelity Test (20260209T004258Z)

- Fonte: `data/reports/cycle_metrics_minute_fused_20260209T004233Z.csv`
- Vetor X (ciclos): `['phi_mean', 'duration_mean', 'components_mean', 'complexity_mean']`
- Vetor Y (daemon): `['daemon_phi_mean', 'daemon_sigma_mean', 'daemon_epsilon_mean', 'daemon_ci_mean']`
- Linhas usadas: 3765

## Resultado
- F_estática (média): -0.105762 ± 0.530584
- F_dinâmica (média): -0.069501 ± 0.465783
- Razão dinâmica/estática: 0.657144
- Melhor lag dinâmico: 0 min (F=-0.069501, n=3765)

## Veredito
**NÃO SUSTENTADA NESTA JANELA (dinâmica < estática)**

## Arquivos
- JSON: `data/reports/trajectory_fidelity_20260209T004258Z.json`
- CSV lag: `data/reports/trajectory_fidelity_lag_20260209T004258Z.csv`
