# Technical Study Compilation (20260218T182531Z)

This file compiles the publication-facing technical scope and result traceability.

## Included Studies
- HIV wrapper functional-cure safe simulation + Qdrant materialization.
- HIV monthly safe cohabitation simulation + Qdrant materialization.
- HIV+SLE 12-month extension simulation + Qdrant materialization.
- Lupus wrapper tolerance simulation + Qdrant materialization.
- Runtime phagocytosis threshold sweep/profile/gate audit.
- Diabetes T2 ingestion and 15-house projection.
- DM2 gut-immune real-data validation (datasets + logs, non-synthetic).
- HIV GWAS + CCR5 rs333 materialization.
- HIV acquisition GWAS meta summary materialization.
- External DM2/Lupus (CSV + tongue image + lupus PDF) extraction wave.

## Quantitative Digest
- hiv_best: scenario=`wrapper_cohab` score=0.8825
- hiv_wrapper_vs_baseline_score_gain_pct=10.79
- hiv_wrapper_vs_baseline_inflammation_drop_pct=98.11
- hiv_wrapper_inert_fraction_pct=20.69
- hiv_m18_wrapper_score=0.8825
- hiv_m18_wrapper_vs_baseline_score_gain_pct=10.79
- hiv_m18_wrapper_vs_baseline_inflammation_drop_pct=98.11
- cohab_best: scenario=`isolated_A` mode=`omnimind_cohabitante_protetivo` index=0.6374
- lupus_best: scenario=`wrapper_tolerance_baff_gate` score=0.7979
- hiv_sle_best: scenario=`adp_enhanced` cohab_score_m12=0.9080
- runtime_gate_global_pass_rate=0.0476
- diabetes_collection_points=3
- diabetes_15houses_points=15
- dm2_gut_immune_realdata_status=ABERTA (glycemic_fields=3, immune_fields=1, microbiome_fields=0, gate_pass_rate=0.0476)
- hiv_gwas_ccr5_points=17 (rows=16)
- hiv_acquisition_meta_rows=5347926 gws_hits=4 top_n=1500
- external_dm2_lupus_points=27 (tongue_images=2750, lupus_docs=3)
- d15_extended_pairs_validated=63 (max_lag=300, bootstrap=300, permutation=300)
- astro_cycle_strength=ROBUST_LOCAL (dominant_lag=240, strong_pairs=20, very_strong_pairs=9)
- desi_local_operational_evidence=False (pending_mentions=False, reports_mentions=True, sdss_pending_mentions=73)
- lya_pdf_probe: exists=True pages_scanned=6 desi_mentions_in_pdf=16
- qdrant_reuse: total=144 used=62 candidate=6 zero_points=24 duplicates=14
- qdrant_cross: schema_opportunities=1 semantic_nonzero_collections=1
- qdrant_followup: leverage_now=6 defer=0 archive_or_merge=12 zero_hold=12
- desi_lya_sample: files=11 collection=`astro_desi_lya_sample_live`
- runtime_snapshot_services_system_user=99/49
- runtime_snapshot_processes_total_root=481/267

## Detailed JSON Analysis
### 2.1 hiv_wrapper (M12 + M18, 72 runs)
- wrapper_cohab: score=0.8825 | inert_fraction=20.69% | inflammation=1.00%
- vs baseline_aggressive: score_gain=10.79% | inflammation_drop=98.11%
- M18 extension executed: wrapper_cohab score=0.8825 | rebound_events_phase3=0.00
- M18 vs baseline_aggressive: score_gain=10.79% | inflammation_drop=98.11%
- gap_resolution: M18 rebound check closed locally in safe computational run.

### 2.2 lupus_wrapper_tolerance
- best scenario: `wrapper_tolerance_baff_gate` score=0.7979
- auto_bad_m12=0.0173 | ifn_alpha_m12=0.2239 | baff_m12=0.1322
- inert_fraction_m12=76.08%

### 2.3 diabetes_t2_15houses
- points_upserted=15 | total_fields=55
- dm2_gut_immune_realdata_status=ABERTA
- realdata_markers: glycemic_fields=3, immune_proxy_fields=1, microbiome_specific_fields=0
- runtime_gate_pass_rate=0.0476
- note: Real-data validation confirms glycemic/immune runtime evidence, but microbiome-specific markers are still absent in local artifacts.

### 2.4 phagocytosis_genomics_15houses
- dataset_records=24 | qdrant_bio_points=2173
- top_genomic_houses=[{'house': 'Epsilon', 'strands_genomic_hits': 88, 'viral_load_hits': 0}, {'house': 'Sigma', 'strands_genomic_hits': 15, 'viral_load_hits': 0}, {'house': 'Aleph', 'strands_genomic_hits': 9, 'viral_load_hits': 0}, {'house': 'Zeta', 'strands_genomic_hits': 9, 'viral_load_hits': 8}, {'house': 'Isfet', 'strands_genomic_hits': 6, 'viral_load_hits': 6}]

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
- gap_astro_cycle_sustainment_validation: status=`FECHADA_LOCAL` note=Local high-sampling cycle sustainment validated with bootstrap/permutation and publication extras rendered.
- gap_dm2_microbiome_wrapper: status=`ABERTA` note=Real-data validation confirms glycemic/immune runtime evidence, but microbiome-specific markers are still absent in local artifacts.
- gap_multi_disease_pack_hiv_dm2_lupus: status=`FECHADA_LOCAL` note=Multi-disease pack completeness validated locally (HIV+DM2+Lupus required components present).
- gap_ensembl_grch38_mapping: status=`FECHADA_LOCAL` note=Ensembl GRCh38 mapper executed on wrapper candidates (gene-symbol mapping coverage achieved in local run).
- gap_uk_biobank_hiv_controllers: status=`BLOQUEADA` note=Needs controlled-access cohort data and user-provided credentials/download.
- gap_wetlab_crispr_wrapper: status=`BLOQUEADA` note=Wet-lab validation is outside software-only pipeline scope.
- gap_wrapper_gene_candidates: status=`EM_REVISAO_LOCAL` note=Local candidate panel generated from HIV GWAS cross+heterogeneity+CHR6 evidence (anchors CCR5/rs333 preserved); pending scientific review.

## D15 Extended Validation (High Sampling)
- run_profile: `max_lag=300`, `bootstrap=300`, `permutation=300`.
- pairs_validated=63
- artifact_json: `data/d15_extended_correlation_validation_compact200_20260218T180530Z.json`
- method_note: d15 houses are treated as operational variables/functions in this runtime model.

## DESI / Official APIs Audit (Local Evidence)
- audit_json: `data/desi_official_apis_audit_20260218T152416Z.json`
- desi_detected_in_pending_tasks=`False`
- desi_detected_in_reports_runtime=`True` (currently from analysis-note artifacts)
- desi_local_operational_evidence=`False`
- sdss_mentions_in_pending_tasks=`73`

## LyA Forest PDF Probe (Local)
- pdf_probe_json: `data/lya_forest_pdf_probe_20260218T152655Z.json`
- exists/pages_scanned: `True/6`
- keyword_counts: `{'sdss': 2, 'eboss': 10, 'desi': 16, 'bao': 8, 'lyman_alpha': 25, 'quasar': 27, 'dla': 0}`

## Qdrant Reuse/Cross Audit (Collections Structure)
- reuse_audit_json: `data/qdrant_collection_reuse_structure_compact200_20260218T153225Z.json`
- schema_overlap_json: `data/qdrant_schema_overlap_20260218T153718Z.json`
- candidate_cross_hits_json: `data/qdrant_candidate_cross_hits_20260218T153415Z.json`
- followup_plan_json: `data/qdrant_collection_followup_plan_20260218T154105Z.json`
- counts: total=144, used=62, candidate=6, zero_points=24, duplicates=14
- cross_opportunities(schema/semantic)=1/1
- followup_counts(leverage/defer/archive/zero_hold)=6/0/12/12

## DESI LyA Minimal Sample (Local Robustness Increment)
- sample_json: `data/desi_lya_sample_materialization_20260218T170112Z.json`
- files_count=11 | qdrant_collection=`astro_desi_lya_sample_live`

## Runtime Infrastructure Snapshot (Operational Evidence)
- snapshot_json: `data/runtime_service_process_snapshot_20260218T145108Z.json`
- services_running_system_user: `99/49`
- processes_total_root: `481/267`
- ports_focus_checked/open_count: `10/10` (details_exposed=False)
- standalone_publication_extras: `docs/publication_extras/runtime_service_process_snapshot_<TS>/` (MD/DOCX/PNG outside zip pack).

## Astro-Bio Cycle Sustainment (Local Robustness)
- sustainment_json: `data/astro_bio_cycle_sustainment_20260218T170121Z.json`
- board: strength=`ROBUST_LOCAL` dominant_lag=`240` strong_pairs=`20` very_strong_pairs=`9`
- mean_abs_r_top_validated=`0.7418`
- extras_outside_zip: `reports_runtime/astro_bio_cycle_heatmap_<TS>.png`, `reports_runtime/astro_bio_fractal_partial_<TS>.png`

## DM2 Gut-Immune Real-Data Validation
- validation_json: `data/dm2_gut_immune_realdata_validation_20260218T182246Z.json`
- decision: `gap_dm2_microbiome_wrapper=ABERTA`
- markers(glycemic/immune/microbiome)=3/1/0

## Ensembl GRCh38 Mapping (Closure Evidence)
- mapping_json: `data/wrapper_candidates_ensembl_grch38_mapping_compact200_20260218T175521Z.json`
- decision: `gap_ensembl_grch38_mapping=FECHADA_LOCAL`

## Multi-disease Pack Validation (Closure Evidence)
- validation_json: `data/multi_disease_pack_validation_compact200_20260218T175507Z.json`
- decision: `gap_multi_disease_pack_hiv_dm2_lupus=FECHADA_LOCAL`

## Wrapper Gene Candidate Panel (Local Review)
- panel_json: `data/wrapper_gene_candidates_panel_compact200_20260218T175521Z.json`
- current_status: `gap_wrapper_gene_candidates=EM_REVISAO_LOCAL`

## Unified Heatmap Validation (Closure Evidence)
- validation_json: `data/hiv_dm2_lupus_15houses_heatmap_validation_compact200_20260218T175507Z.json`
- decision: `gap_heatmap_15houses_gwas_hiv_dm2_lupus=FECHADA_LOCAL`

## HIV M18 Rebound Closure (Safe Run)
- assessment_json: `data/hiv_m18_rebound_gap_assessment_compact200_20260218T133845Z.json`
- decision: `gap_m18_rebound_hiv=FECHADA_LOCAL`

## Federation Continuity Reference (Zenodo v3)
- reference_doi: `10.5281/zenodo.18396039`.
- scope_note: historical federation continuity anchor; contextual prior, not replacement for current-run statistics.
- historical_snapshot: Jan 27, 2026 logs recorded `15 views / 0 downloads` for DOI v3 in that specific time-window.
- fractal_vision_reference_doi: `10.5281/zenodo.18437517`.

## Technical-Scientific Criteria (2026, Operational)
- D15 labels are runtime operators (functions over logs/metrics), not allegorical labels.
- Acceptance rule: reproducibility + explicit uncertainty (CI/permutation/lag declaration).
- Evidence rule: claims must map to concrete artifacts (JSON/CSV/figures) and sample sizes.

## Data Governance / LGPD-GDPR Technical Criteria
- Minimum-storage policy in development and publication boundary with aggregate outputs only.
- Controlled datasets remain blocked until legal/ethical prerequisites are met.
- Encryption/key-separation and deletion/right-to-erasure paths stay mandatory.


## Result Files
- `TECHNICAL_REPORT.md`
- `RESULTS_SUMMARY.json`
- `data/*.json`

## Notes
- Content is computational/systems research output only.
- No clinical claim and no patient-level data are included.
