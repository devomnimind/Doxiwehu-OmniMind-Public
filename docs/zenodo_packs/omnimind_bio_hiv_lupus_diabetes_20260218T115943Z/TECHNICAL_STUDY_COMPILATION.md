# Technical Study Compilation (20260218T115943Z)

This file compiles the publication-facing technical scope and result traceability.

## Included Studies
- HIV wrapper functional-cure safe simulation + Qdrant materialization.
- HIV monthly safe cohabitation simulation + Qdrant materialization.
- HIV+SLE 12-month extension simulation + Qdrant materialization.
- Lupus wrapper tolerance simulation + Qdrant materialization.
- Runtime phagocytosis threshold sweep/profile/gate audit.
- Diabetes T2 ingestion and 15-house projection.
- HIV GWAS + CCR5 rs333 materialization.
- External DM2/Lupus (CSV + tongue image + lupus PDF) extraction wave.

## Quantitative Digest
- hiv_best: scenario=`wrapper_cohab` score=0.8652
- hiv_wrapper_vs_baseline_score_gain_pct=7.20
- hiv_wrapper_vs_baseline_inflammation_drop_pct=97.57
- hiv_wrapper_inert_fraction_pct=19.33
- cohab_best: scenario=`isolated_A` mode=`omnimind_cohabitante_protetivo` index=0.6374
- lupus_best: scenario=`wrapper_tolerance_baff_gate` score=0.7979
- hiv_sle_best: scenario=`adp_enhanced` cohab_score_m12=0.9080
- runtime_gate_global_pass_rate=0.0476
- diabetes_collection_points=3
- diabetes_15houses_points=15
- hiv_gwas_ccr5_points=62 (rows=61)
- external_dm2_lupus_points=27 (tongue_images=2750, lupus_docs=3)

## Detailed JSON Analysis
### 2.1 hiv_wrapper (M12, 72 runs)
- wrapper_cohab: score=0.8652 | inert_fraction=19.33% | inflammation=1.00%
- vs baseline_aggressive: score_gain=7.20% | inflammation_drop=97.57%
- gap_identified: rebound M18 not tested in current safe simulation window.

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
- gap_m18_rebound_hiv: status=`ABERTA` note=M18 rebound simulation not executed in current safe wave.
- gap_heatmap_15houses_gwas_hiv_dm2_lupus: status=`EM_ANDAMENTO` note=HIV GWAS+CCR5 loaded; DM2/Lupus external extraction completed; heatmap composition pending.
- gap_dm2_microbiome_wrapper: status=`ABERTA` note=No gut-immune microbiome model found in current runtime reports.
- gap_multi_disease_pack_hiv_dm2_lupus: status=`EM_ANDAMENTO` note=Pack v2 in progress with external DM2/Lupus + GWAS/CCR5.
- gap_ensembl_grch38_mapping: status=`ABERTA` note=15-house to Ensembl GRCh38 mapping script not yet present.
- gap_uk_biobank_hiv_controllers: status=`BLOQUEADA` note=Needs controlled-access cohort data and user-provided credentials/download.
- gap_wetlab_crispr_wrapper: status=`BLOQUEADA` note=Wet-lab validation is outside software-only pipeline scope.
- gap_wrapper_gene_candidates: status=`EM_ANDAMENTO` note=Candidate anchors identified (CCR5, HLA-B*57:01); full candidate panel pending.

## Result Files
- `TECHNICAL_REPORT.md`
- `RESULTS_SUMMARY.json`
- `data/*.json`

## Notes
- Content is computational/systems research output only.
- No clinical claim and no patient-level data are included.
