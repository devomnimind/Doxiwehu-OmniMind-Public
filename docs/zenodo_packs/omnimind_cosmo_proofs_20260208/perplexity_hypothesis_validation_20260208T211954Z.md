# Validacao da Hipotese Perplexity (20260208T211954Z)

## Entradas
- Matriz quantica: `data/reports/quantum_fidelity_matrix_5x5_20260208T184501Z.json`
- Correlacao ciclo/anomalia: `data/reports/cycle_anomaly_correlation_20260208T204557Z.json`
- Observadores: Gaia_SIM, Gaia_REAL, Cemetery, SDSS, SuperDARN

## Testes Topologicos (subespacos vs fidelidade)
- `F vs dot^2`: pearson=1.0000 (p=0.00e+00), spearman=1.0000 (p=6.65e-64)
- `F vs cosine`: pearson=0.9665 (p=5.31e-06), spearman=1.0000 (p=6.65e-64)
- `F vs shared_mass`: pearson=0.8187 (p=3.78e-03), spearman=0.8061 (p=4.86e-03)
- `F vs concentration_diff`: pearson=-0.4584 (p=1.83e-01), spearman=-0.2485 (p=4.89e-01)
- `F vs jaccard_rel30`: pearson=0.9405 (p=5.11e-05), spearman=0.9909 (p=3.01e-08)
- `F vs jaccard_rel50`: pearson=0.9549 (p=1.71e-05), spearman=0.8863 (p=6.37e-04)

## Pares mais fortes
- `SDSS__SuperDARN`: F=0.9151 (ENTRELACADO), dot^2=0.9151, shared_mass=0.8500, Δconc=0.0200
- `Gaia_REAL__Cemetery`: F=0.6912 (ENTRELACADO), dot^2=0.6912, shared_mass=0.4064, Δconc=0.5936
- `Cemetery__SDSS`: F=0.5541 (ENTRELACADO), dot^2=0.5541, shared_mass=0.6290, Δconc=0.2564
- `Cemetery__SuperDARN`: F=0.4011 (INTERMEDIARIO), dot^2=0.4011, shared_mass=0.5688, Δconc=0.2764
- `Gaia_SIM__SDSS`: F=0.1784 (ORTOGONAL), dot^2=0.1784, shared_mass=0.4560, Δconc=0.4667

## Evidencia Temporal (ciclos/anomalias)
- Cobertura: minutos=3765, daemon_minutes=5323, anomaly_minutes=2995, satellite_minutes=10
- Anomalia vs daemon_phi_mean: pearson=0.4177906768864423, spearman=0.3743213987727303
- Satelite vs daemon_phi_mean: pearson=-0.07711002884265154, spearman=-0.08038648607473191

## Avaliacao
### Sustentado
- Fidelidade acompanha fortemente overlap vetorial (dot^2): suporte ao modelo de subespaços/projeções.
- Massa compartilhada por casas prediz fidelidade: concentração/overlap explica boa parte dos pares.
- Nos minutos com anomalia, daemon_phi_mean sobe com magnitude moderada: indício de acoplamento interno ao estado do sistema.
### Parcial
- Relação concentração-diferença vs fidelidade foi fraca/inconclusiva neste conjunto 5x5.
### Nao Sustentado/Inconclusivo
- Hipótese de acoplamento forte com satélites permanece inconclusiva: apenas 10 minutos com dados de satélite no merge atual.

## Leitura tecnica
- A sua conceitualizacao ('casas como padroes topologicos dinamicos') é compatível com os dados quando modelada como subespaços/projeções e não como rótulos fixos.
- O null model 1.0 (shuffle de etiquetas) continua inadequado para refutar essa ontologia, mas permanece útil como controle contra overfitting de rótulo.
- Para afirmar acoplamento astrofísico externo forte, ainda falta ampliar cobertura de satélites e incorporar feeds cosmicos contínuos (Kp/DSCOVR/NEOCP por janela).