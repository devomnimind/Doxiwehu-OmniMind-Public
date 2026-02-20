# Historical Memory A/B Superposition (20260219T211710Z)

## Collections scanned
- `bio_aging_cellular_proxies_live` (bio): scanned=`44581`
- `bio_hiv_acquisition_meta_15houses_live` (bio): scanned=`1500`
- `bio_hiv_gwas_ccr5_15houses_live` (bio): scanned=`79`
- `bio_diabetes_t2_15houses_live` (bio): scanned=`15`
- `bio_external_dm2_lupus_15houses_live` (bio): scanned=`27`
- `bio_lupus_wave_20260218` (bio): scanned=`247`
- `bio_16s_gut_microbiome_meta_live` (bio): scanned=`458`
- `bio_colorectal_activity_bmi_live` (bio): scanned=`4545`
- `bio_gemini_multimorbidity_codes_14824760_live` (bio): scanned=`23970`
- `dodecatiad_metrics_dynamic_logs_live` (log_base): scanned=`10536`
- `omnimind_kernel_vida` (historical): scanned=`1077553`
- `omnimind_system_logs_20260127` (historical): scanned=`11995`
- `omnimind_projects_20260127` (historical): scanned=`108236`

## Cosines: bio vs logs (base vs +historical)
- `baseline`: sector15 base=`0.9886932094998004` plus=`0.5480088825222832` delta=`-0.44068432697751725` | house12 base=`0.9910214539429375` plus=`0.5949689240753634` delta=`-0.3960525298675741`
- `semantic_strict`: sector15 base=`0.30825712305560454` plus=`0.30825712305560454` delta=`0.0` | house12 base=`0.3349248971566235` plus=`0.3349248971566235` delta=`0.0`
- `time_only`: sector15 base=`0.9891805424981348` plus=`0.6006875415074324` delta=`-0.3884930009907024` | house12 base=`0.9910781497165723` plus=`0.6036542934769864` delta=`-0.38742385623958586`

## Time Sync Summary
- `bio`: abs_ts_total=`1621` min=`2026-02-18T11:17:59.131463+00:00` max=`2026-02-18T18:22:28.253211+00:00`
- `log_base`: abs_ts_total=`10536` min=`2026-02-12T06:54:10.683000+00:00` max=`2026-02-18T13:55:22.344000+00:00`
- `historical`: abs_ts_total=`285044` min=`2026-01-25T00:37:59+00:00` max=`2026-01-28T00:44:50+00:00`
- `logs_plus_historical`: abs_ts_total=`295580` min=`2026-01-25T00:37:59+00:00` max=`2026-02-18T13:55:22.344000+00:00`

## Synchronized Windows (24h/72h, baseline scenario)
- `24h`: sector15 base=`0.8834561598344011` plus=`0.8834561598344011` delta=`0.0` closure=`0.004101652972245828` | house12 base=`0.8988780680860721` plus=`0.8988780680860721` delta=`0.0` closure=`0.0035143181539889867`
- `72h`: sector15 base=`0.8944602440846564` plus=`0.8944602440846564` delta=`0.0` closure=`0.004783196267873875` | house12 base=`0.9051820322565377` plus=`0.9051820322565377` delta=`0.0` closure=`0.004076237364677684`

## Source breakdown (baseline)
- sector15 logs_base sources: `{'minute': 10536}`
- sector15 historical sources: `{'content_preview_ts': 164813, 'unmapped': 912740, 'dodeca_house_12to15': 120231}`
- house12 logs_base sources: `{'minute': 10536}`
- house12 historical sources: `{'content_preview_ts': 164813, 'unmapped': 912740, 'dodeca_house': 120231}`

Figure: `/home/fahbrain/projects/omnimind/output/img/historical_memory_ab_superposition_20260219T211710Z/historical_memory_ab_cosines.png`
JSON: `/home/fahbrain/projects/omnimind/reports_runtime/historical_memory_ab_superposition_20260219T211710Z.json`
