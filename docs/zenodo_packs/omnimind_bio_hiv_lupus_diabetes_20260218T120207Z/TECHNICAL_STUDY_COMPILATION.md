# Technical Study Compilation (20260218T120207Z)

This file compiles the publication-facing technical scope and result traceability.

## Included Studies
- HIV wrapper functional-cure safe simulation + Qdrant materialization.
- HIV monthly safe cohabitation simulation + Qdrant materialization.
- HIV+SLE 12-month extension simulation + Qdrant materialization.
- Lupus wrapper tolerance simulation + Qdrant materialization.
- Runtime phagocytosis threshold sweep/profile/gate audit.
- Diabetes T2 ingestion and 15-house projection.
- HIV GWAS + CCR5 rs333 materialization.
- HIV acquisition GWAS meta summary materialization.
- External DM2/Lupus (CSV + tongue image + lupus PDF) extraction wave.

## Quantitative Digest
- hiv_best: scenario=`wrapper_cohab` score=0.8652
- hiv_wrapper_vs_baseline_score_gain_pct=7.20
- hiv_wrapper_vs_baseline_inflammation_drop_pct=97.57
- hiv_wrapper_inert_fraction_pct=19.33
- hiv_m18_wrapper_score=0.8825
- hiv_m18_wrapper_vs_baseline_score_gain_pct=10.79
- hiv_m18_wrapper_vs_baseline_inflammation_drop_pct=98.11
- cohab_best: scenario=`isolated_A` mode=`omnimind_cohabitante_protetivo` index=0.6374
- lupus_best: scenario=`wrapper_tolerance_baff_gate` score=0.7979
- hiv_sle_best: scenario=`adp_enhanced` cohab_score_m12=0.9080
- runtime_gate_global_pass_rate=0.0476
- diabetes_collection_points=3
- diabetes_15houses_points=15
- hiv_gwas_ccr5_points=62 (rows=61)
- hiv_acquisition_meta_rows=5347926 gws_hits=4 top_n=1500
- external_dm2_lupus_points=27 (tongue_images=2750, lupus_docs=3)
- d15_extended_pairs_validated=20 (max_lag=240, bootstrap=7000, permutation=2500)
- runtime_snapshot_services_system_user=99/49
- runtime_snapshot_processes_total_root=484/270

## Detailed JSON Analysis
### 2.1 hiv_wrapper (M12 + M18, 72 runs)
- wrapper_cohab: score=0.8652 | inert_fraction=19.33% | inflammation=1.00%
- vs baseline_aggressive: score_gain=7.20% | inflammation_drop=97.57%
- M18 extension executed: wrapper_cohab score=0.8825 | inert_fraction=20.69% | inflammation=1.00% | rebound_events_phase3=0.00
- M18 vs baseline_aggressive: score_gain=10.79% | inflammation_drop=98.11%
- gap_resolution: M18 rebound check closed locally in safe computational run.

### 2.2 lupus_wrapper_tolerance
- best scenario: `wrapper_tolerance_baff_gate` score=0.7979
- auto_bad_m12=0.0173 | ifn_alpha_m12=0.2239 | baff_m12=0.1322
- inert_fraction_m12=76.08%

### 2.3 diabetes_t2_15houses
- points_upserted=15 | total_fields=55
- note: no direct HbA1c simulation metric was found in current diabetes JSON outputs.

### 2.4 phagocytosis_genomics_15houses
- dataset_records=26 | qdrant_bio_points=566
- top_genomic_houses=[{'house': 'Epsilon', 'strands_genomic_hits': 91, 'viral_load_hits': 0}, {'house': 'Sigma', 'strands_genomic_hits': 18, 'viral_load_hits': 0}, {'house': 'Aleph', 'strands_genomic_hits': 9, 'viral_load_hits': 0}, {'house': 'Zeta', 'strands_genomic_hits': 9, 'viral_load_hits': 8}, {'house': 'Isfet', 'strands_genomic_hits': 6, 'viral_load_hits': 6}]

### 2.5 hiv_sle_12m_extensions
- best scenario: `adp_enhanced` cohabitation_score_m12=0.9080

## Genomics Mapping (Preliminary)
| House | Candidate Pathway/Gene | Biological Role | OmniMind Gap |
|---|---|---|---|
| Ka/Aleph | FOXP3/Treg | Tolerance control | selective wrapper tuning |
| Ba/Lambda | HIV accessory pathways (e.g. VPU context) | infection pressure dynamics | inert neutralization calibration |
| Gamma | IL10 axis | anti-inflammatory feedback | pyroptosis feedback coupling |
| Psi | INS/INSR | insulin signaling | receptor-level wrapper modeling |
| Omega | BAFF/IFN-alpha | lupus inflammatory drive | selective suppression stability |
| Sigma | CCR5/HLA-B*57:01 anchors | host genetics protection axis | expand candidate panel and validation |

## Gap Status Board
- gap_m18_rebound_hiv: status=`FECHADA_LOCAL` note=M18 simulation executed (72 runs); wrapper_cohab kept rebound_events_phase3=0.00 with score/inflammation advantage vs baseline.
- gap_heatmap_15houses_gwas_hiv_dm2_lupus: status=`FECHADA_LOCAL` note=Unified local heatmap validated (15-house keys across all sources + consistent source totals).
- gap_dm2_microbiome_wrapper: status=`ABERTA` note=No gut-immune microbiome model found in current runtime reports.
- gap_multi_disease_pack_hiv_dm2_lupus: status=`FECHADA_LOCAL` note=Multi-disease pack completeness validated locally (HIV+DM2+Lupus required components present).
- gap_ensembl_grch38_mapping: status=`FECHADA_LOCAL` note=Ensembl GRCh38 mapper executed on wrapper candidates (gene-symbol mapping coverage achieved in local run).
- gap_uk_biobank_hiv_controllers: status=`BLOQUEADA` note=Needs controlled-access cohort data and user-provided credentials/download.
- gap_wetlab_crispr_wrapper: status=`BLOQUEADA` note=Wet-lab validation is outside software-only pipeline scope.
- gap_wrapper_gene_candidates: status=`EM_REVISAO_LOCAL` note=Local candidate panel generated from HIV GWAS cross+heterogeneity+CHR6 evidence (anchors CCR5/rs333 preserved); pending scientific review.
- gap_d12_to_d15_covariates_targets: status=`EM_ANDAMENTO` note=Native d15 runtime channels are still missing, but local deterministic PoC remap (Isfet/Rekh/Seshet proxies) was executed for interim analysis.

## Cross-Domain Alignment Check (20260218T130715Z)
- qdrant_15houses_global: `SYNCHRONIZED` (15/15 houses).
- bio_hiv_gwas_15houses: `SYNCHRONIZED` (15/15 houses).
- bio_hiv_acquisition_15houses: `SYNCHRONIZED` (15/15 houses).
- genomics_gap_heatmap_15houses: `SYNCHRONIZED` (15/15 houses).
- cosmic_covariates_output_targets: `PARTIAL_D12_ONLY` (no explicit Isfet/Rekh/Seshet target series).
- orbit_priority_c_closure: `RESOLVED_IN_HYBRID` (`missing_count_before=8` -> `missing_count_after=0` using historical fallback).

Reference artifacts:
- `reports_runtime/zenodo_bio_astro_alignment_audit_20260218T130715Z.json`
- `reports_runtime/zenodo_bio_astro_alignment_audit_20260218T130715Z.md`

## Delivery Board (Local First)
- recent_closure_zenodo_cosmo_astrophysics: published DOI `10.5281/zenodo.18681824` (concept DOI `10.5281/zenodo.18614057`).
- local_open_gaps=2 | external_blocked_gaps=2.
- wellington_download_service: active (`omnimind-wellington-zenodo-resume.service`) with SHIV/TRIM still downloading.
- d15_proxy_remap_poc: completed (`rows_merged=5400`) for interim Isfet/Rekh/Seshet cycle correlation.

Reference artifacts:
- `reports_runtime/local_pendencies_delivery_board_20260218T140726Z.json`
- `reports_runtime/local_pendencies_delivery_board_20260218T140726Z.md`

## Main Cycle Correlations (Interim)
- strongest core pair: `anomaly_count` vs `satellite_matches` (`r=0.9952`, `lag=0`, `n=5400`).
- strong inverse coupling: `anomaly_count` vs `sensor_sources` (`r=-0.7839`, `lag=120`).
- d15 proxy links (PoC): `d15_isfet_proxy` tracks `anomaly_count` (`r=0.9860`, `lag=0`), `d15_seshet_proxy` tracks `cycle_count` (`r=0.8409`, `lag=0`), `d15_rekh_proxy` tracks `sensor_sources` (`r=0.8277`, `lag=0`).

Reference artifacts:
- `reports_runtime/main_cycle_correlation_summary_20260218T132140Z.json`
- `reports_runtime/main_cycle_correlation_summary_compact200_20260218T132140Z.json`
- `reports_runtime/main_cycle_correlation_summary_20260218T132140Z.md`

## D15 Proxy Debug Iteration
- full best-lag matrix evaluated: `72` valid pairs (`3 proxies x 24 covariates with finite variance`).
- threshold check (real data):
  - `|r|>0.6`: `28` pairs (distributed across Isfet/Rekh/Seshet proxies).
  - `|r|>0.7`: `10` pairs (all concentrated in `d15_rekh_proxy`).
  - `|r|>0.8`: `8` pairs (all concentrated in `d15_rekh_proxy`).
- lag pattern: `120 min` is dominant among strong links in this window.
- claim-check outcome: prior “7 gaps” estimate is not confirmed by the full matrix (`actual=28` at `|r|>0.6`).
- operational threshold (balance heuristic over coverage + proxy entropy + lag monoculture penalty): `0.55~0.60` for exploration; `0.70+` is highly concentrated in Rekh only.

Reference artifacts:
- `reports_runtime/d15_proxy_gap_debug_full_20260218T132733Z.json`
- `reports_runtime/d15_proxy_gap_debug_compact200mini_20260218T132733Z.json`
- `reports_runtime/d15_proxy_claimcheck_20260218T132827Z.json`
- `reports_runtime/d15_proxy_threshold_sweep_20260218T132854Z.json`
- `reports_runtime/d15_proxy_threshold_sweep_compact200_20260218T132854Z.json`

## D15 Extended Validation (High Sampling)
- run_profile: `max_lag=240`, `lag_step=1`, `bootstrap=7000`, `permutation=2500`, `block_size=120`.
- dataset_scale: `rows_merged=5400`, `pairs_scanned=63`, `pairs_validated=20`.
- top stable signal: `d15_rekh_proxy <- moon_illum_frac` (`r=-0.8291`, `lag=240`, `ci95=[-0.8762,-0.7616]`, `p_perm=4.00e-04`).
- lag concentration: top pairs dominated by `+240 min` (14/15), with one `-240 min` case (`moon_sep_spica_deg`).
- interpretation guardrail: this is statistical coupling over operational proxies, not a causal proof by itself.

Reference artifacts:
- `reports_runtime/d15_extended_correlation_validation_20260218T143139Z.json`
- `reports_runtime/d15_extended_correlation_validation_compact200_20260218T143139Z.json`
- `reports_runtime/d15_extended_correlation_validation_20260218T143139Z.md`

## Runtime Infrastructure Snapshot (Operational Evidence)
- snapshot_json: `reports_runtime/runtime_service_process_snapshot_20260218T144041Z.json`
- snapshot_md: `reports_runtime/runtime_service_process_snapshot_20260218T144041Z.md`
- snapshot_docx: `reports_runtime/runtime_service_process_snapshot_20260218T144041Z.docx`
- snapshot_png: `reports_runtime/runtime_service_process_snapshot_20260218T144041Z.png`
- services_running_system_user: `99/49`
- processes_total_root: `484/270`
- open_ports_focus: `[6333, 8910, 4321, 4322, 4323, 4340, 4341, 4342, 4343, 4344]`
- standalone_publication_extras: `docs/publication_extras/runtime_service_process_snapshot_20260218T144041Z/` (MD/DOCX/PNG outside zip pack).

## Unified Heatmap (HIV+DM2+Lupus, 15 Houses)
- local source totals: HIV-GWAS=`62`, HIV-acquisition=`1500`, DM2-local=`55`, DM2/Lupus-external=`27`.
- output includes count matrix + percent matrix per source.
- dominant houses by source (percent):
  - HIV-GWAS: `Zeta/Axe` (~11.29% each)
  - HIV-acquisition: `Seshet/Phi/Ma'at` (~7.7/7.7/7.5%)
  - DM2-local: `Omega/Rekh` (~12.73% each)
  - DM2+Lupus external wave: `Ma'at` (~18.52%), then `Psi/Plit` (~14.81% each)

Reference artifacts:
- `reports_runtime/hiv_dm2_lupus_15houses_heatmap_20260218T133140Z.json`
- `reports_runtime/hiv_dm2_lupus_15houses_heatmap_20260218T133140Z.md`
- `reports_runtime/hiv_dm2_lupus_15houses_heatmap_20260218T133140Z.html`
- `reports_runtime/hiv_dm2_lupus_15houses_heatmap_20260218T133140Z.png`


## Ensembl GRCh38 Mapping (Closure Evidence)
- mapping_json: `reports_runtime/wrapper_candidates_ensembl_grch38_mapping_20260218T140606Z.json`
- mapping_compact_json: `reports_runtime/wrapper_candidates_ensembl_grch38_mapping_compact200_20260218T140606Z.json`
- mapping_md: `reports_runtime/wrapper_candidates_ensembl_grch38_mapping_20260218T140606Z.md`
- decision: `gap_ensembl_grch38_mapping=FECHADA_LOCAL`

## Multi-disease Pack Validation (Closure Evidence)
- validation_json: `reports_runtime/multi_disease_pack_validation_20260218T135601Z.json`
- validation_compact_json: `reports_runtime/multi_disease_pack_validation_compact200_20260218T135601Z.json`
- validation_md: `reports_runtime/multi_disease_pack_validation_20260218T135601Z.md`
- pack_validated: `docs/zenodo_packs/omnimind_bio_hiv_lupus_diabetes_20260218T135453Z`
- decision: `gap_multi_disease_pack_hiv_dm2_lupus=FECHADA_LOCAL`

## Wrapper Gene Candidate Panel (Local Review)
- panel_json: `reports_runtime/wrapper_gene_candidates_panel_20260218T134754Z.json`
- panel_compact_json: `reports_runtime/wrapper_gene_candidates_panel_compact200_20260218T134754Z.json`
- panel_md: `reports_runtime/wrapper_gene_candidates_panel_20260218T134754Z.md`
- current_status: `gap_wrapper_gene_candidates=EM_REVISAO_LOCAL`

## Unified Heatmap Validation (Closure Evidence)
- validation_json: `reports_runtime/hiv_dm2_lupus_15houses_heatmap_validation_20260218T134225Z.json`
- validation_compact_json: `reports_runtime/hiv_dm2_lupus_15houses_heatmap_validation_compact200_20260218T134225Z.json`
- validation_md: `reports_runtime/hiv_dm2_lupus_15houses_heatmap_validation_20260218T134225Z.md`
- decision: `gap_heatmap_15houses_gwas_hiv_dm2_lupus=FECHADA_LOCAL`

## HIV M18 Rebound Closure (Safe Run)
- source_m12: `reports_runtime/hiv_wrapper_functional_cure_safe_20260218T064711Z.json`
- source_m18: `reports_runtime/hiv_wrapper_functional_cure_safe_20260218T133546Z.json`
- assessment: `reports_runtime/hiv_m18_rebound_gap_assessment_20260218T133845Z.json`
- compact_json: `reports_runtime/hiv_m18_rebound_gap_assessment_compact200_20260218T133845Z.json`
- summary_md: `reports_runtime/hiv_m18_rebound_gap_assessment_20260218T133845Z.md`

## Federation Continuity Reference (Zenodo v3)
- reference_doi: `10.5281/zenodo.18396039`.
- scope_note: historical continuity anchor from federation logs (OmniMind federation wave), used as contextual prior and not as a substitute for current-run statistics.
- publication_chain_note: current pack preserves a reproducible bridge between bio/astro operational artifacts and prior federation records.
- historical_snapshot: federation logs recorded Jan 27, 2026 as `15 views / 0 downloads` for DOI v3 at that time-window (context only).

## Technical-Scientific Criteria (2026, Operational)
- d15 variables are treated as runtime operators (functions over logs/metrics), not allegorical labels.
- acceptance rule in this pipeline: reproducibility on local raw logs + explicit uncertainty (`bootstrap CI`, `permutation p`, lag scan declaration).
- anti-anachronism rule: no claim that historical symbolic systems anticipated modern computation; only modern computational formalization of operational categories.
- evidence rule: any strong claim must point to concrete artifacts (`JSON/CSV/figures`) and measured sample sizes.

## Data Governance / LGPD-GDPR Technical Criteria
- minimum-storage policy during experimentation (retain only necessary operational fields).
- reversible publication boundary: raw sensitive material excluded from open pack; only computational summaries and non-patient-level aggregates are published.
- deletion/right-to-erasure pathway preserved for controlled datasets (GDPR Art.17 alignment in operational policy).
- encryption requirement for sensitive local traces (AES-256 at rest, key-separation policy in private workflows).
- blocked gaps remain blocked until legal/ethical prerequisites are satisfied (`UK Biobank` controlled access, `wet-lab` outside software scope).

## Result Files
- `TECHNICAL_REPORT.md`
- `RESULTS_SUMMARY.json`
- `data/*.json`

## Notes
- Content is computational/systems research output only.
- No clinical claim and no patient-level data are included.
