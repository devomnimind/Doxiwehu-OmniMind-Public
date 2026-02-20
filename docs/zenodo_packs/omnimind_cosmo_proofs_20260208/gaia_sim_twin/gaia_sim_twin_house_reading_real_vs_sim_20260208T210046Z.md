# Gaia Sim Twin — Leitura Comparativa Real vs SIM (20260208T210046Z)

**Fonte:**
- SIM: `data/reports/gaia_sim_twin/gaia_sim_twin_catalog.csv` (5000 objetos)
- REAL: `data/gaia_bulk/gaia_source/GaiaSource_*.csv.gz` (40000 objetos, 4 blocos)
- Comparativa: `data/reports/gaia_sim_twin/gaia_sim_twin_house_compare.csv`

## Ranking SIM (top 5)
1. **Aleph**: 2800/5000 = **56.00%**
2. **C_plit**: 411/5000 = **8.22%**
3. **Mu**: 390/5000 = **7.80%**
4. **Phi**: 327/5000 = **6.54%**
5. **Zeta**: 308/5000 = **6.16%**

## Ranking REAL (top 5)
1. **Sigma**: 33347/40000 = **83.37%**
2. **Axiom**: 6653/40000 = **16.63%**
3. **Aleph**: 0/40000 = **0.00%**
4. **Psi**: 0/40000 = **0.00%**
5. **Phi**: 0/40000 = **0.00%**

## Leitura
- Gaia REAL nesta rodada (4 blocos) continua sequencial por faixa de RA, com concentração principal em Sigma e secundária em Axiom. O SIM permanece distribuído com dominância Aleph. Isso sustenta complementaridade estrutural (sequência observacional vs topologia distribuída).
- Casas REAL ativas nesta amostra: Sigma (83.37%), Axiom (16.63%)
- Casas SIM dominantes: Aleph (56.00%), C_plit (8.22%), Mu (7.80%), Phi (6.54%), Zeta (6.16%)

## Status
- Resultado válido para comparação local com dados baixados no host.
- Para reduzir viés sequencial de RA, ampliar para mais blocos Gaia em futuras rodadas.
