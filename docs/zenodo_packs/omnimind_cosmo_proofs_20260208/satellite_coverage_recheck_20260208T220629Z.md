# Recheck Satélite x Ciclos (20260208T220629Z)

- Ciclos: `data/reports/cycle_metrics_minute_20260208T204557Z.csv`
- Sat antigo: `data/reports/anomaly_satellite_cross_20260208T143912Z.json`
- Sat novo: `data/reports/anomaly_satellite_cross_20260208T215410Z.json`

## Contagens
- Antigo: overlap=10 | overlap_anomalia=9 | max_matches=73 | mean_nonzero=71.50
- Novo: overlap=10 | overlap_anomalia=9 | max_matches=202 | mean_nonzero=199.50

## Conclusão
- Mudança de minutos sobrepostos: 0
- Mesmo com mais satélites por timestamp, a interseção temporal com a série de ciclos permaneceu baixa.
- Gargalo: janela temporal de interseção (não quantidade de satélites).
- Recomendação: aumentar janela temporal de anomalias/ciclos ou gerar cross por período contínuo para elevar satellite_minutes.

JSON: `data/reports/satellite_coverage_recheck_20260208T220629Z.json`