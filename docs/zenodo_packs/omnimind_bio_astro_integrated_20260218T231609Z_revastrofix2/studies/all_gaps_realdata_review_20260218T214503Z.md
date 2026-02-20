# Real-data Gaps Review (20260218T214503Z)

## Inputs
- d15: `/home/fahbrain/projects/omnimind/reports_runtime/d15_extended_correlation_validation_20260218T184552Z.json`
- dm2: `/home/fahbrain/projects/omnimind/reports_runtime/dm2_gut_immune_realdata_validation_20260218T204707Z.json`
- multi-disease: `/home/fahbrain/projects/omnimind/reports_runtime/multi_disease_pack_validation_20260218T211252Z.json`
- horizon review: `/home/fahbrain/projects/omnimind/reports_runtime/accelerated_structure_horizon_thermo_review_20260218T205849Z.json`
- antigravity: `/home/fahbrain/projects/omnimind/reports_runtime/antigravity_theory_validation_20260209T194118Z.json`
- desi_lya: `/home/fahbrain/projects/omnimind/reports_runtime/desi_lya_sample_materialization_20260218T170112Z.json`
- cosmic resonance: `/home/fahbrain/projects/omnimind/reports_runtime/cosmic_resonance_candidates_20260217T002406Z.json`
- cosmo registry: `/home/fahbrain/projects/omnimind/reports_runtime/cosmo_objects_registry_internal_20260211T202630Z.json`
- sdss17 fallback: `/home/fahbrain/projects/omnimind/reports_runtime/sdss17_service_qdrant_fallback_recheck_20260216T233933Z.json`
- orbit multihorizon: `/home/fahbrain/projects/omnimind/reports_runtime/orbit_queue_priority_c_multihorizon_20260216T220416Z.json`

## Core real-data counts
- merged rows: `5400`
- d15 validated pairs: `63`
- dm2 microbiome external points total: `1143`

## Core pair lag result
- best lag (moon_illum_frac vs d15_rekh_proxy): `{'lag_min': 300, 'r': -0.8323412104628806, 'n': 5100}`

## Granger (d15_rekh_proxy -> moon_illum_frac)
- lag=60 min | F=0.038880 | p=1
- lag=120 min | F=0.034696 | p=1
- lag=180 min | F=0.015665 | p=1
- lag=240 min | F=0.019952 | p=1
- lag=300 min | F=0.003179 | p=1

## Astrophysical experimental track (independent from bio wrappers)
- horizon files count: `3`
- DESI LYA files count: `11`
- DESI LYA total size bytes: `1799354`
- cosmic resonance top covariates count: `12`
- cosmo registry confirmed objects: `4`
- note: Astrophysical experiments (objects/asteroids/SDSS17/Horizon/antigravity/LYA) are tracked as their own runtime line, not as 'astro of disease'.

## Simulation classification from pack checker
- simulated components: `['hiv_wrapper_sim', 'hiv_cohab_sim', 'hiv_sle_sim', 'lupus_sim']`
- real components: `['diabetes_15houses', 'hiv_gwas', 'hiv_acquisition_meta', 'dm2_lupus_external_wave', 'm18_rebound_assessment', 'heatmap_validation', 'wrapper_gene_panel', 'wrapper_ensembl_mapping']`

## Figures
- `/home/fahbrain/projects/omnimind/output/img/all_gaps_realdata_20260218T214503Z/all_gaps_realdata_heatmap.png`
- `/home/fahbrain/projects/omnimind/output/img/all_gaps_realdata_20260218T214503Z/lag_ccf_d15rekh_moonillum.png`
- `/home/fahbrain/projects/omnimind/output/img/all_gaps_realdata_20260218T214503Z/acf_pacf_d15rekh_moonillum.png`

JSON: `reports_runtime/all_gaps_realdata_review_20260218T214503Z.json`
