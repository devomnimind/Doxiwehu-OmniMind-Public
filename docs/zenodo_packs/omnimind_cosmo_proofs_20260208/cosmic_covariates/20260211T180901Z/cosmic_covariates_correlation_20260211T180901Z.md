# Cosmic Covariates Correlation (20260211T180901Z)

## Inputs
- metrics_csv: `reports_runtime/cycle_metrics_minute_neurocore_10k_20260211T130531Z.csv`
- covariates_csv: `reports_runtime/cosmic_covariates_20260211T180848Z.csv`

## Top Pairs by |pearson| (best lag)
- venus_az_deg vs sensor_event_count: lag=-80 | pearson=-0.664474613464213 (p=0.0) | spearman=-0.6651745793584268 (p=0.0) | n=4339 | edge_best=False
- mercury_az_deg vs sensor_event_count: lag=-100 | pearson=-0.663505841625235 (p=0.0) | spearman=-0.6651748440855506 (p=0.0) | n=4339 | edge_best=False
- sun_az_deg vs sensor_event_count: lag=-45 | pearson=-0.6629452813372536 (p=0.0) | spearman=-0.6651830011395756 (p=0.0) | n=4339 | edge_best=False
- mars_az_deg vs sensor_event_count: lag=-15 | pearson=-0.6587890344425349 (p=0.0) | spearman=-0.6651609511482719 (p=0.0) | n=4339 | edge_best=False
- moon_phase_deg vs sensor_event_count: lag=-120 | pearson=-0.6274203433962192 (p=0.0) | spearman=-0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- moon_alt_deg vs sensor_event_count: lag=120 | pearson=0.623918717744442 (p=0.0) | spearman=0.6701509468918014 (p=0.0) | n=4312 | edge_best=True
- moon_sep_spica_deg vs sensor_event_count: lag=-120 | pearson=0.608209079798392 (p=0.0) | spearman=0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- moon_sep_regulus_deg vs sensor_event_count: lag=-120 | pearson=0.6068994491605165 (p=0.0) | spearman=0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- moon_sep_antares_deg vs sensor_event_count: lag=-120 | pearson=-0.6067438467010553 (p=0.0) | spearman=-0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- moon_sep_beehive_m44_deg vs sensor_event_count: lag=-120 | pearson=0.6065814985961568 (p=0.0) | spearman=0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- moon_sep_mars_deg vs sensor_event_count: lag=-120 | pearson=-0.6039033277096739 (p=0.0) | spearman=-0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- moon_illum_frac vs sensor_event_count: lag=-120 | pearson=-0.6032983025427211 (p=0.0) | spearman=-0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- sun_moon_sep_deg vs sensor_event_count: lag=-120 | pearson=-0.6028049634953151 (p=0.0) | spearman=-0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- moon_sep_venus_deg vs sensor_event_count: lag=-120 | pearson=-0.6026459904914196 (p=0.0) | spearman=-0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- moon_sep_mercury_deg vs sensor_event_count: lag=-120 | pearson=-0.6006133757520191 (p=0.0) | spearman=-0.6651698951937344 (p=0.0) | n=4339 | edge_best=True
- tide_moon_local vs sensor_event_count: lag=120 | pearson=0.3526708547246004 (p=1.699684830067643e-126) | spearman=0.3714810907621004 (p=3.421558486058495e-141) | n=4312 | edge_best=True
- mars_az_deg vs sensor_sources: lag=-15 | pearson=-0.3498578811040111 (p=3.7743868226144945e-125) | spearman=-0.369753603035701 (p=1.1539179660690215e-140) | n=4339 | edge_best=False
- moon_sep_mercury_deg vs sensor_sources: lag=55 | pearson=-0.34614372240986685 (p=3.2963940460988357e-122) | spearman=-0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- moon_sep_venus_deg vs sensor_sources: lag=55 | pearson=-0.34594862711720975 (p=4.597726756851165e-122) | spearman=-0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- moon_illum_frac vs sensor_sources: lag=55 | pearson=-0.3459084397133733 (p=4.923755823472352e-122) | spearman=-0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- sun_moon_sep_deg vs sensor_sources: lag=55 | pearson=-0.3457765622693057 (p=6.16457545017404e-122) | spearman=-0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- moon_sep_mars_deg vs sensor_sources: lag=55 | pearson=-0.345719068234476 (p=6.79894542337684e-122) | spearman=-0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- moon_sep_spica_deg vs sensor_sources: lag=55 | pearson=0.3455355444057498 (p=9.293219763323474e-122) | spearman=0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- moon_sep_antares_deg vs sensor_sources: lag=55 | pearson=-0.34548144021404564 (p=1.0189700363104684e-121) | spearman=-0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- moon_sep_regulus_deg vs sensor_sources: lag=55 | pearson=0.3454130870741778 (p=1.14466514958637e-121) | spearman=0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- moon_sep_beehive_m44_deg vs sensor_sources: lag=55 | pearson=0.34540408465331596 (p=1.1623337344431757e-121) | spearman=0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- sun_az_deg vs sensor_sources: lag=-45 | pearson=-0.33951173013491787 (p=1.6320016311948016e-117) | spearman=-0.3697675241476153 (p=1.1244176389482686e-140) | n=4339 | edge_best=False
- moon_phase_deg vs sensor_sources: lag=55 | pearson=-0.33729941122115253 (p=9.240859221959172e-116) | spearman=-0.3713841414760204 (p=8.603853317981367e-142) | n=4333 | edge_best=False
- moon_alt_deg vs sensor_sources: lag=55 | pearson=0.3342824161711075 (p=1.3100885637150486e-113) | spearman=0.3755238236041734 (p=3.553926536198422e-145) | n=4333 | edge_best=False
- tide_total_local vs sensor_event_count: lag=30 | pearson=0.33384599375590157 (p=2.2356852509787073e-113) | spearman=0.34773482774096054 (p=1.784691230396956e-123) | n=4336 | edge_best=False
- venus_az_deg vs sensor_sources: lag=-80 | pearson=-0.3275944776534644 (p=4.497468529946989e-109) | spearman=-0.3697956518980666 (p=1.0670891311412005e-140) | n=4339 | edge_best=False
- mercury_az_deg vs sensor_sources: lag=-100 | pearson=-0.3195044453433187 (p=1.4810138534478114e-103) | spearman=-0.3697852955507836 (p=1.0878494339676396e-140) | n=4339 | edge_best=False
- moon_alt_deg vs daemon_health_mean: lag=-85 | pearson=-0.3031723054148874 (p=1.8417685552257486e-180) | spearman=-0.5073123784076333 (p=0.0) | n=8513 | edge_best=False
- mars_az_deg vs daemon_health_mean: lag=-85 | pearson=0.3016546692667534 (p=1.3633041894736673e-178) | spearman=0.49242270450566844 (p=0.0) | n=8513 | edge_best=False
- sun_az_deg vs daemon_health_mean: lag=-110 | pearson=0.30040423389017595 (p=1.5151397120027475e-176) | spearman=0.4934559820818404 (p=0.0) | n=8488 | edge_best=False
- venus_az_deg vs daemon_health_mean: lag=-80 | pearson=0.29781632513873446 (p=5.146181401905302e-174) | spearman=0.4915370809159332 (p=0.0) | n=8518 | edge_best=False
- mercury_az_deg vs daemon_health_mean: lag=-100 | pearson=0.29635436522518593 (p=7.502152237825604e-172) | spearman=0.4935102339287515 (p=0.0) | n=8498 | edge_best=False
- moon_phase_deg vs daemon_health_mean: lag=-120 | pearson=0.2831042705523675 (p=5.271630733381506e-156) | spearman=0.48604289522149025 (p=0.0) | n=8478 | edge_best=True
- moon_sep_spica_deg vs daemon_health_mean: lag=-120 | pearson=-0.2817908095654805 (p=1.6142466677686298e-154) | spearman=-0.48604289522149025 (p=0.0) | n=8478 | edge_best=True
- moon_sep_regulus_deg vs daemon_health_mean: lag=-120 | pearson=-0.28136806830149913 (p=4.8365079265275155e-154) | spearman=-0.48604289522149025 (p=0.0) | n=8478 | edge_best=True

## Diff Sanity (top 20 by |pearson| on first differences)
- Δmars_az_deg vs Δd12_mu: lag=0 | pearson=0.7149344031707386 (p=0.0) | spearman=-0.00890598943099722 (p=0.44435011914419453) | n=7378 | edge_best=False
- Δsun_az_deg vs Δd12_cplit: lag=-35 | pearson=-0.7108610643452165 (p=0.0) | spearman=-0.013300839471554969 (p=0.2542171785841845) | n=7350 | edge_best=False
- Δsun_az_deg vs Δd12_c_split: lag=-35 | pearson=-0.7108610643452165 (p=0.0) | spearman=-0.013300839471554969 (p=0.2542171785841845) | n=7350 | edge_best=False
- Δvenus_az_deg vs Δd12_cplit: lag=-70 | pearson=0.7101852857262747 (p=0.0) | spearman=0.020962413584641137 (p=0.07301144620719786) | n=7315 | edge_best=False
- Δvenus_az_deg vs Δd12_c_split: lag=-70 | pearson=0.7101852857262747 (p=0.0) | spearman=0.020962413584641137 (p=0.07301144620719786) | n=7315 | edge_best=False
- Δmercury_az_deg vs Δd12_cplit: lag=-90 | pearson=-0.7094206762994995 (p=0.0) | spearman=-0.0019401739156910457 (p=0.8683881435282296) | n=7297 | edge_best=False
- Δmercury_az_deg vs Δd12_c_split: lag=-90 | pearson=-0.7094206762994995 (p=0.0) | spearman=-0.0019401739156910457 (p=0.8683881435282296) | n=7297 | edge_best=False
- Δsun_az_deg vs Δd12_aleph: lag=40 | pearson=-0.39326297943495 (p=1.6681206927586965e-270) | spearman=-0.0020913395322575768 (p=0.8577106946582396) | n=7352 | edge_best=False
- Δmercury_az_deg vs Δd12_aleph: lag=-15 | pearson=-0.3921823546656058 (p=2.0748809905589698e-269) | spearman=-0.015224329220633867 (p=0.19138660023076867) | n=7366 | edge_best=False
- Δsun_az_deg vs Δdaemon_csi_mean: lag=-5 | pearson=0.3195298669133521 (p=2.862147266085474e-178) | spearman=0.001911345594018871 (p=0.8683075045045026) | n=7528 | edge_best=False
- Δmercury_az_deg vs Δdaemon_csi_mean: lag=-60 | pearson=0.318884271011521 (p=3.0894785740977635e-176) | spearman=0.012967452453204496 (p=0.26235142872678857) | n=7473 | edge_best=False
- Δmars_az_deg vs Δd12_aleph: lag=70 | pearson=-0.2763685782116091 (p=1.2965026820141977e-128) | spearman=0.0036250684788237467 (p=0.7563414455560276) | n=7329 | edge_best=False
- Δmercury_az_deg vs Δd12_epsilon: lag=-15 | pearson=0.21267001747321362 (p=3.2223569786833426e-76) | spearman=0.013725534868522044 (p=0.23847205093683008) | n=7378 | edge_best=False
- Δmercury_az_deg vs Δd12_sigma: lag=5 | pearson=0.18109243635956182 (p=1.5321640692761641e-55) | spearman=0.012407494152796041 (p=0.2860798223163446) | n=7394 | edge_best=False
- Δsun_az_deg vs Δd12_sigma: lag=60 | pearson=0.18082058652529684 (p=4.815266195382048e-55) | spearman=0.0016575186052597247 (p=0.8870332377985978) | n=7348 | edge_best=False
- Δsun_az_deg vs Δdaemon_gns_mean: lag=45 | pearson=0.16765704277629764 (p=1.770359041147061e-48) | spearman=-0.0066601465351781575 (p=0.5638592304555636) | n=7511 | edge_best=False
- Δmercury_az_deg vs Δdaemon_gns_mean: lag=-10 | pearson=0.16747203920289372 (p=1.897055323054709e-48) | spearman=0.004669440143298503 (p=0.68552171118639) | n=7523 | edge_best=False
- Δvenus_az_deg vs Δd12_aleph: lag=5 | pearson=0.16467775708012694 (p=5.175312835097927e-46) | spearman=0.0024364036623659518 (p=0.834260545357034) | n=7378 | edge_best=False
- Δsun_az_deg vs Δdaemon_ci_mean: lag=45 | pearson=0.15927007643914012 (p=7.3085821560497875e-44) | spearman=-0.016593865560300104 (p=0.15043858772893326) | n=7511 | edge_best=False
- Δmercury_az_deg vs Δdaemon_ci_mean: lag=-10 | pearson=0.15896743506550629 (p=9.093544702065011e-44) | spearman=-0.00701515107129143 (p=0.5429440177001277) | n=7523 | edge_best=False

## Note
Correlações aqui não implicam causalidade: covariáveis astronômicas são altamente periódicas e podem correlacionar com rotinas operacionais (carga, janelas de manutenção, operador).

JSON: `reports_runtime/cosmic_covariates_correlation_20260211T180901Z.json`
