# OmniMind Integrated Bio+Astro Local Evidence Pack (20260218T231145Z)

Technical local-evidence package for an integrated study across:
- biomedical tracks (HIV, lupus, T2D/microbiome, aging proxies),
- astrophysical tracks (SDSS/DESI/LYA/JWST-horizon and derivatives),
- runtime/log tracks (Qdrant + process time series).
- social/federation track (Witness event stream + watermarks + territory snapshot + hash-alien index; no raw URLs).

Astrophysical baseline continuity: DOI `10.5281/zenodo.18681824`.

## Purpose
Document methodology, execution, and traceability for bio+astro analyses in a local environment, with emphasis on reproducible pipelines and consistency auditing.

## Structure
- `data/`: JSON/MD reports, audits, materialization logs, and execution diagnostics.
- `images/`: technical inspection figures (heatmaps, distributions, overlap diagnostics).
- `studies/`: main study in direct-view formats (`md`, `docx`, `pdf`).
- `RESULTS_SUMMARY.json`: cycle-level local status summary.
- `PACK_MANIFEST.json`: file inventory + SHA-256 integrity.

## Doxihewu manuscript (canonical)
- Official file for reading/citation:
  - `studies/DOXIHEWU_OMNIMIND_manuscrito_canonico_20260219.md`
- Canonical-vs-draft policy:
  - `studies/DOXIHEWU_VERSIONAMENTO_CANONICO_20260220.md`
  - `data/doxihewu_version_registry_20260220.json`

## Quick reading path (recommended)
1. Scope and methods:
   - `README_EN.md`
   - `TECHNICAL_REPORT.md`
2. Main closure artifacts:
   - `data/astro_d15_15houses_broadened_cross_20260218T235601Z.json`
   - `data/aging_studies_integration_realdata_20260219T125603Z.json`
3. Method controls (avoid temporal-overlap inflation):
   - `data/bio_logs_cosine_contamination_diagnosis_20260219T203902Z.json`
   - `data/historical_memory_ab_superposition_20260219T211710Z.json`
   - `data/tier2_memory_async_closure_20260219T212146Z.json`
4. Social/federation event-stream:
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
5. Figures:
   - `images/all_gaps_realdata_heatmap.png`
   - `images/historical_memory_ab_cosines.png`
   - `images/fig_jwst_analysis.png`

## Provenance and rigor
- Artifacts are explicitly labeled by provenance (`real-data-local`, `scenario-simulation`, `mixed`) in internal reports.
- No silent mixing between empirical evidence and scenario modeling.

## Scope (public clarity)
- This pack does **not** claim biological consciousness proof or a closed cosmological causality proof.
- This pack **does** provide an auditable technical trail: measurements, cross-domain analyses, explicit limits, and peer-review-ready materials.

## Language note
- Portuguese originals are preserved.
- English support files in this package:
  - `README_EN.md`
  - `TECHNICAL_REPORT_EN.md`
  - `ZENODO_HEADER_DESCRIPTION_PT_EN.md`
