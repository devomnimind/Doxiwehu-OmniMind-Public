# OmniMind Integrated Bio+Astro Local Evidence Pack (20260218T231145Z)

Pack técnico de evidência local para estudo integrado entre:
- trilhas biomédicas (HIV, lupus, DM2/microbioma, proxies de aging),
- trilhas astrofísicas (SDSS/DESI/LYA/JWST-horizon e derivados),
- trilhas operacionais de runtime/logs (Qdrant + séries de processo).
- trilha social/federativa (event-stream do Witness + watermarks + territory snapshot + hash-alien index, sem URLs cruas).

Continuidade da linha astrofísica-base: DOI `10.5281/zenodo.18681824`.

## Objetivo
Documentar metodologia, execução e rastreabilidade de análises bio+astro em ambiente local, com foco em reprodutibilidade de pipeline e auditoria de consistência.

## Estrutura
- `data/`: relatórios JSON/MD, auditorias, materializações e diagnósticos de execução.
- `images/`: figuras de inspeção técnica (heatmaps, distribuições, diagnósticos de overlap).
- `studies/`: versão de estudo em formatos de leitura direta (`md`, `docx`, `pdf`).
- `RESULTS_SUMMARY.json`: resumo de status local do ciclo.
- `PACK_MANIFEST.json`: inventário + integridade SHA-256 dos arquivos do pack.

## Manuscrito Doxihewu (canônico)
- Arquivo oficial para leitura/citação:
  - `studies/DOXIHEWU_OMNIMIND_manuscrito_canonico_20260219.md`
- Política de versionamento (canônico vs rascunhos):
  - `studies/DOXIHEWU_VERSIONAMENTO_CANONICO_20260220.md`
  - `data/doxihewu_version_registry_20260220.json`

## Roteiro de leitura rapida (ordem sugerida)
1. Contexto e escopo:
   - `README.md`
   - `TECHNICAL_REPORT.md`
2. Fechamento principal bio+astro:
   - `data/astro_d15_15houses_broadened_cross_20260218T235601Z.json`
   - `data/aging_studies_integration_realdata_20260219T125603Z.json`
3. Controles metodologicos (evitar falso positivo de sincronia temporal):
   - `data/bio_logs_cosine_contamination_diagnosis_20260219T203902Z.json`
   - `data/historical_memory_ab_superposition_20260219T211710Z.json`
   - `data/tier2_memory_async_closure_20260219T212146Z.json`
4. Trilha social/federativa (dataset/event-stream):
   - `data/triad_domain_scope_status_20260220T115738Z.json`
   - `data/social_federation/federation_social_dataset_summary_20260220T115413Z.json`
   - `studies/federation_perplexity_split_screen_experience_20260220T120430Z.md`
   - `studies/federation_proxy_latency_window_summary_20260220T123743Z.md`
   - `studies/federation_proxy_latency_window_summary_20260220T125048Z.md`
   - `studies/federation_dual_webapp_lag_gap_analysis_20260220T130344Z.md`
   - `studies/federation_proxy_latency_window_summary_20260220T130745Z.md`
   - `studies/federation_dual_webapp_lag_gap_analysis_20260220T131257Z.md`
   - `studies/federation_proxy_latency_window_summary_20260220T133450Z.md`
   - `studies/federation_dual_webapp_lag_gap_analysis_20260220T134004Z.md`
   - `studies/federation_proxy_latency_window_summary_20260220T140555Z.md`
   - `studies/federation_dual_webapp_lag_gap_analysis_20260220T141313Z.md`
   - `studies/federation_dual_webapp_lag_gap_analysis_20260220T141851Z.md`
   - `studies/federation_dual_webapp_lag_gap_analysis_20260220T142218Z.md`
   - `studies/federation_proxy_latency_window_summary_20260220T142553Z.md`
   - `studies/federation_dual_webapp_lag_gap_analysis_20260220T143106Z.md`
   - `data/social_federation/federation_webapp_metrics_d15_status_20260220T124512Z.json`
5. Figuras para inspeção:
   - `images/all_gaps_realdata_heatmap.png`
   - `images/historical_memory_ab_cosines.png`
   - `images/fig_jwst_analysis.png`
6. Integridade e reprodutibilidade:
   - `PACK_MANIFEST.json`
   - `data/zenodo_pack_consistency_audit_20260220T001250Z.json`

## Proveniência e rigor
- Artefatos rotulados por proveniência (`real-data-local`, `scenario-simulation`, `mixed`) nos relatórios internos.
- Sem mistura silenciosa entre evidência empírica e cenário.

## Escopo (clareza pública)
- Este pack **não** reivindica “prova de consciência biológica” nem causalidade cosmológica fechada.
- Este pack **sim** entrega: trilha técnica auditável, medições, cruzamentos, limitações explícitas e base para revisão por pares.

## Versões em inglês
- `README_EN.md`
- `TECHNICAL_REPORT_EN.md`
- `ZENODO_HEADER_DESCRIPTION_PT_EN.md` (texto pronto para descrição no cabeçalho da página Zenodo)
