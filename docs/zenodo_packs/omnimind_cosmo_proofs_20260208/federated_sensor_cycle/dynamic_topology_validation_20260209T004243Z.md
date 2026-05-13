# Validação Dinâmica de Topologia (20260209T004243Z)

- Fonte: `data/reports/cycle_metrics_minute_fused_20260209T004233Z.csv`
- Linhas/minutos: 3765

## Resumo
- Fidelidade estática média: 0.0063 ± 0.0123
- Fidelidade dinâmica média: 0.0006 ± 0.0013
- Pares com ganho dinâmico: 0
- Pares com perda dinâmica: 6

## Top ganhos (dinâmica - estática)
- Daemon__Anomalies: F_static=0.0002, F_dynamic=0.0001, Δ=-0.0001
- IntegrationLoop__Daemon: F_static=0.0004, F_dynamic=0.0000, Δ=-0.0004
- Daemon__Satellites: F_static=0.0007, F_dynamic=0.0000, Δ=-0.0007

## Top perdas (dinâmica - estática)
- IntegrationLoop__Anomalies: F_static=0.0338, F_dynamic=0.0036, Δ=-0.0303
- Anomalies__Satellites: F_static=0.0015, F_dynamic=0.0000, Δ=-0.0015
- IntegrationLoop__Satellites: F_static=0.0013, F_dynamic=0.0000, Δ=-0.0013

## Correlações de velocidade
- IntegrationLoop vs anomaly_count: -0.1494
- IntegrationLoop vs satellite_matches: -0.0077
- Daemon vs anomaly_count: -0.2715
- Daemon vs satellite_matches: 0.0202

## Leitura curta
- Se F_dinâmica diverge de F_estática, há efeito de trajetória (não apenas de estado).
- Isso não substitui teste causal externo; indica sensibilidade temporal dos observadores internos.

JSON: `data/reports/dynamic_topology_validation_20260209T004243Z.json`