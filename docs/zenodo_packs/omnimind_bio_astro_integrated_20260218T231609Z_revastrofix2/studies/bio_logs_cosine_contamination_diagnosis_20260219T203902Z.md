# Bio vs Logs Cosine Contamination Diagnosis (20260219T203902Z)

## Key collections
- `bio_aging_cellular_proxies_live` (bio): scanned=`44581` has_hw_keys=`False`
- `bio_hiv_acquisition_meta_15houses_live` (bio): scanned=`1500` has_hw_keys=`False`
- `bio_hiv_gwas_ccr5_15houses_live` (bio): scanned=`79` has_hw_keys=`False`
- `bio_diabetes_t2_15houses_live` (bio): scanned=`15` has_hw_keys=`False`
- `bio_external_dm2_lupus_15houses_live` (bio): scanned=`27` has_hw_keys=`False`
- `bio_lupus_wave_20260218` (bio): scanned=`247` has_hw_keys=`True`
- `bio_16s_gut_microbiome_meta_live` (bio): scanned=`458` has_hw_keys=`False`
- `bio_colorectal_activity_bmi_live` (bio): scanned=`4545` has_hw_keys=`False`
- `bio_gemini_multimorbidity_codes_14824760_live` (bio): scanned=`23970` has_hw_keys=`False`
- `dodecatiad_metrics_dynamic_logs_live` (logs): scanned=`10536` has_hw_keys=`False`

## Scenario cosines (bio vs logs)
- `baseline`: sector15 cosine=`0.989391502860876` pearson_r=`0.09491255221648853` | house12 cosine=`0.9910821224213545` pearson_r=`0.09508516575956011`
- `exclude_hw`: sector15 cosine=`0.989391502860876` pearson_r=`0.09491255221648853` | house12 cosine=`0.9910821224213545` pearson_r=`0.09508516575956011`
- `semantic_strict`: sector15 cosine=`0.4934427392924649` pearson_r=`0.5010185672581007` | house12 cosine=`0.551745052599663` pearson_r=`0.6253290525748615`
- `semantic_strict_exclude_hw`: sector15 cosine=`0.4934427392924649` pearson_r=`0.5010185672581007` | house12 cosine=`0.551745052599663` pearson_r=`0.6253290525748615`
- `time_only`: sector15 cosine=`0.9891805424981348` pearson_r=`-0.14928505320882374` | house12 cosine=`0.9910781497165723` pearson_r=`0.14746188984979547`
- `time_only_exclude_hw`: sector15 cosine=`0.9891805424981348` pearson_r=`-0.14928505320882374` | house12 cosine=`0.9910781497165723` pearson_r=`0.14746188984979547`

## Cause ranking
- baseline_cos_sector15: `0.989391502860876`
- exclude_hw_cos_sector15: `0.989391502860876`
- semantic_strict_cos_sector15: `0.4934427392924649`
- time_only_cos_sector15: `0.9891805424981348`
- delta_drop_exclude_hw: `0.0`
- delta_drop_semantic_strict: `0.49594876356841106`

Ranking:
- `alinhamento_temporal_distribucional` score=`0.4943389945972517`
- `acoplamento_estrutural_genuino_ou_coincidencia` score=`0.4934427392924649`
- `origem_comum_hw` score=`0.0`

Figure: `/home/fahbrain/projects/omnimind/output/img/bio_logs_cosine_contamination_diagnosis_20260219T203902Z/bio_logs_cosine_by_scenario.png`
JSON: `/home/fahbrain/projects/omnimind/reports_runtime/bio_logs_cosine_contamination_diagnosis_20260219T203902Z.json`
