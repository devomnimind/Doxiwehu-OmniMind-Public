# Cosmic Covariates Correlation (20260210T213143Z)

## Inputs
- metrics_csv: `reports_runtime/space_weather_merged_20260209T104949Z.csv`
- covariates_csv: `reports_runtime/cosmic_covariates_20260210T205330Z.csv`

## Top Pairs by |pearson| (best lag)
- moon_sep_spica_deg vs sensor_sources: lag=120 | pearson=0.7647878272264022 (p=9.617810203531455e-219) | spearman=0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- moon_illum_frac vs sensor_sources: lag=120 | pearson=-0.7562687365776579 (p=3.6085206104331727e-211) | spearman=-0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- moon_sep_mercury_deg vs sensor_sources: lag=120 | pearson=-0.7525470430259829 (p=5.871570282764472e-208) | spearman=-0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- moon_sep_venus_deg vs sensor_sources: lag=120 | pearson=-0.751879462539369 (p=2.1814639186684925e-207) | spearman=-0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- sun_moon_sep_deg vs sensor_sources: lag=120 | pearson=-0.7516922524421024 (p=3.149669653120018e-207) | spearman=-0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- moon_sep_mars_deg vs sensor_sources: lag=120 | pearson=-0.7514633677105671 (p=4.932850249306733e-207) | spearman=-0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- moon_sep_beehive_m44_deg vs sensor_sources: lag=120 | pearson=0.7507797294559619 (p=1.8782903182674194e-206) | spearman=0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- moon_sep_antares_deg vs sensor_sources: lag=120 | pearson=-0.7507647396140885 (p=1.934075813009342e-206) | spearman=-0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- moon_sep_regulus_deg vs sensor_sources: lag=120 | pearson=0.7507597795107801 (p=1.9528966427471436e-206) | spearman=0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- moon_illum_frac vs satellite_matches: lag=55 | pearson=0.7113806213810755 (p=0.0) | spearman=0.5463189067941392 (p=0.0) | n=5345 | edge_best=False
- moon_sep_spica_deg vs anomaly_count: lag=-120 | pearson=-0.7032391671854277 (p=0.0) | spearman=-0.6502423560511429 (p=0.0) | n=5280 | edge_best=True
- moon_illum_frac vs anomaly_count: lag=120 | pearson=0.7021734150713608 (p=0.0) | spearman=0.6882996995236328 (p=0.0) | n=5280 | edge_best=True
- moon_phase_deg vs sensor_sources: lag=120 | pearson=-0.7017426690532302 (p=3.451203308523031e-169) | spearman=-0.8382181727552184 (p=6.7190803526915214e-301) | n=1136 | edge_best=True
- moon_sep_spica_deg vs sensor_event_count: lag=-15 | pearson=0.694278273203339 (p=4.926166544074929e-162) | spearman=0.8354298670782615 (p=3.673179477090619e-293) | n=1121 | edge_best=False
- moon_sep_mercury_deg vs satellite_matches: lag=55 | pearson=0.6924253239719219 (p=0.0) | spearman=0.5463189067941392 (p=0.0) | n=5345 | edge_best=False
- sun_moon_sep_deg vs satellite_matches: lag=55 | pearson=0.6923210642194547 (p=0.0) | spearman=0.5463189067941392 (p=0.0) | n=5345 | edge_best=False
- moon_sep_mars_deg vs satellite_matches: lag=55 | pearson=0.692216024609464 (p=0.0) | spearman=0.5463189067941392 (p=0.0) | n=5345 | edge_best=False
- moon_sep_beehive_m44_deg vs satellite_matches: lag=60 | pearson=-0.6921869112017935 (p=0.0) | spearman=-0.5454283532951472 (p=0.0) | n=5340 | edge_best=False
- moon_sep_antares_deg vs satellite_matches: lag=60 | pearson=0.6921304055147273 (p=0.0) | spearman=0.5454283532951472 (p=0.0) | n=5340 | edge_best=False
- moon_sep_regulus_deg vs satellite_matches: lag=60 | pearson=-0.6921163576370255 (p=0.0) | spearman=-0.5454283532951472 (p=0.0) | n=5340 | edge_best=False
- moon_sep_venus_deg vs satellite_matches: lag=55 | pearson=0.6920973237501225 (p=0.0) | spearman=0.5463189067941392 (p=0.0) | n=5345 | edge_best=False
- moon_illum_frac vs sensor_event_count: lag=-15 | pearson=-0.6884779022259226 (p=2.690242113146439e-158) | spearman=-0.8351551934875288 (p=8.590846929953749e-293) | n=1121 | edge_best=False
- moon_sep_spica_deg vs satellite_matches: lag=-120 | pearson=-0.6861620126739324 (p=0.0) | spearman=-0.3254456105339438 (p=1.6458468043049198e-130) | n=5280 | edge_best=True
- moon_sep_mercury_deg vs sensor_event_count: lag=-15 | pearson=-0.6844874084139082 (p=8.916250307635018e-156) | spearman=-0.8351551934875288 (p=8.590846929953749e-293) | n=1121 | edge_best=False
- moon_sep_regulus_deg vs sensor_event_count: lag=-15 | pearson=0.6843642923774711 (p=1.0648723888370036e-155) | spearman=0.8351551934875288 (p=8.590846929953749e-293) | n=1121 | edge_best=False
- moon_sep_venus_deg vs sensor_event_count: lag=-15 | pearson=-0.684355270882713 (p=1.0788145399363977e-155) | spearman=-0.8351551934875288 (p=8.590846929953749e-293) | n=1121 | edge_best=False
- moon_sep_antares_deg vs sensor_event_count: lag=-15 | pearson=-0.6842899460347764 (p=1.1853506122285015e-155) | spearman=-0.8351551934875288 (p=8.590846929953749e-293) | n=1121 | edge_best=False
- moon_sep_beehive_m44_deg vs sensor_event_count: lag=-15 | pearson=0.6842369798044596 (p=1.279384850918296e-155) | spearman=0.8351551934875288 (p=8.590846929953749e-293) | n=1121 | edge_best=False
- moon_sep_mars_deg vs sensor_event_count: lag=-15 | pearson=-0.6841777592636331 (p=1.3933560499640824e-155) | spearman=-0.8351551934875288 (p=8.590846929953749e-293) | n=1121 | edge_best=False
- sun_moon_sep_deg vs sensor_event_count: lag=-15 | pearson=-0.6840629844136878 (p=1.643858289847564e-155) | spearman=-0.8351551934875288 (p=8.590846929953749e-293) | n=1121 | edge_best=False
- moon_sep_beehive_m44_deg vs anomaly_count: lag=120 | pearson=-0.6822401680353578 (p=0.0) | spearman=-0.6882996995236328 (p=0.0) | n=5280 | edge_best=True
- moon_sep_antares_deg vs anomaly_count: lag=120 | pearson=0.6821881973504759 (p=0.0) | spearman=0.6882996995236328 (p=0.0) | n=5280 | edge_best=True
- moon_sep_regulus_deg vs anomaly_count: lag=120 | pearson=-0.6821729484304355 (p=0.0) | spearman=-0.6882996995236328 (p=0.0) | n=5280 | edge_best=True
- sun_moon_sep_deg vs anomaly_count: lag=120 | pearson=0.6821305198563514 (p=0.0) | spearman=0.6882996995236328 (p=0.0) | n=5280 | edge_best=True
- moon_sep_mars_deg vs anomaly_count: lag=120 | pearson=0.6820847104561416 (p=0.0) | spearman=0.6882996995236328 (p=0.0) | n=5280 | edge_best=True
- moon_sep_mercury_deg vs anomaly_count: lag=120 | pearson=0.6820267661948407 (p=0.0) | spearman=0.6882996995236328 (p=0.0) | n=5280 | edge_best=True
- moon_sep_venus_deg vs anomaly_count: lag=120 | pearson=0.6818434722373254 (p=0.0) | spearman=0.6882996995236328 (p=0.0) | n=5280 | edge_best=True
- moon_phase_deg vs sensor_event_count: lag=-15 | pearson=-0.6421773292409562 (p=2.36540600280685e-131) | spearman=-0.8351551934875288 (p=8.590846929953749e-293) | n=1121 | edge_best=False
- moon_near_spica vs d12_sync_axe: lag=60 | pearson=0.6323460794077531 (p=0.0) | spearman=0.4212005103771603 (p=6.564746521912267e-149) | n=3461 | edge_best=False
- moon_phase_deg vs satellite_matches: lag=70 | pearson=0.6208351776257788 (p=0.0) | spearman=0.5431646906520997 (p=0.0) | n=5330 | edge_best=False

## Diff Sanity (top 20 by |pearson| on first differences)
- Δmoon_phase_deg vs Δd12_sigma: lag=-30 | pearson=-0.288594530342322 (p=4.323485675087171e-51) | spearman=-0.06982974693939027 (p=0.00036435332512031076) | n=2602 | edge_best=False
- Δmoon_sep_regulus_deg vs Δd12_sigma: lag=-55 | pearson=0.24785725483676846 (p=1.9646506799677875e-37) | spearman=0.009774451360545063 (p=0.6196488581976209) | n=2581 | edge_best=False
- Δmoon_sep_antares_deg vs Δd12_sigma: lag=-55 | pearson=-0.24745051623714404 (p=2.595280509303596e-37) | spearman=-0.009765112223446013 (p=0.6199834504485666) | n=2581 | edge_best=False
- Δmoon_sep_beehive_m44_deg vs Δd12_sigma: lag=-55 | pearson=0.2473093582773347 (p=2.858184053287055e-37) | spearman=0.009621540130250192 (p=0.6251370564885284) | n=2581 | edge_best=False
- Δmoon_sep_mars_deg vs Δd12_sigma: lag=-35 | pearson=-0.24365507690789273 (p=2.0782137013597672e-36) | spearman=-0.014619131787022104 (p=0.4564631814495057) | n=2597 | edge_best=False
- Δsun_moon_sep_deg vs Δd12_sigma: lag=-35 | pearson=-0.24228181112922179 (p=5.244914912497038e-36) | spearman=-0.014406915078857043 (p=0.46302669399205665) | n=2597 | edge_best=False
- Δmoon_sep_venus_deg vs Δd12_sigma: lag=-35 | pearson=-0.24208229019690747 (p=5.9971027957241256e-36) | spearman=-0.014840207629438051 (p=0.4496816146466872) | n=2597 | edge_best=False
- Δmoon_sep_mercury_deg vs Δd12_sigma: lag=-35 | pearson=-0.23914311815050754 (p=4.257661675306174e-35) | spearman=-0.014704388987271251 (p=0.45384110853428206) | n=2597 | edge_best=False
- Δmars_az_deg vs Δanomaly_count: lag=110 | pearson=0.2303236611757218 (p=1.2540098736619704e-64) | spearman=0.030620501253891 (p=0.025954800598819508) | n=5289 | edge_best=False
- Δvenus_az_deg vs Δanomaly_count: lag=50 | pearson=0.22609416397221271 (p=5.730878698676897e-63) | spearman=0.030336404886159272 (p=0.026507045355672575) | n=5349 | edge_best=False
- Δmercury_az_deg vs Δanomaly_count: lag=30 | pearson=-0.22546695899367228 (p=7.560279566014642e-63) | spearman=-0.011444829757379715 (p=0.40178673443537416) | n=5369 | edge_best=False
- Δmars_az_deg vs Δsatellite_matches: lag=85 | pearson=0.2242034465958058 (p=1.5723607138709414e-61) | spearman=0.012959649636564076 (p=0.3448940637421205) | n=5314 | edge_best=False
- Δvenus_az_deg vs Δsatellite_matches: lag=50 | pearson=0.2077171972198975 (p=3.228493870925367e-53) | spearman=0.00939381459891944 (p=0.49215288765896503) | n=5349 | edge_best=False
- Δmercury_az_deg vs Δsatellite_matches: lag=30 | pearson=-0.2062563603954412 (p=1.13770127427294e-52) | spearman=0.01529035281143542 (p=0.26263635423352183) | n=5369 | edge_best=False
- Δmoon_illum_frac vs Δd12_sigma: lag=-35 | pearson=-0.19761763303410643 (p=2.8032273163708207e-24) | spearman=-0.004285291011902201 (p=0.8272128319990755) | n=2597 | edge_best=False
- Δmoon_sep_spica_deg vs Δd12_sigma: lag=-55 | pearson=-0.19640800616776982 (p=7.373860038831629e-24) | spearman=-0.07365355220224103 (p=0.0001802959211648141) | n=2581 | edge_best=False
- Δmoon_phase_deg vs Δd12_aleph: lag=60 | pearson=-0.1560384155173666 (p=9.205770827713e-16) | spearman=0.0011130059905693364 (p=0.9545645467688639) | n=2623 | edge_best=False
- Δsun_az_deg vs Δd12_sigma: lag=-25 | pearson=-0.1515874876324563 (p=7.185861923633949e-15) | spearman=-0.03893372859315376 (p=0.046843849108066826) | n=2607 | edge_best=False
- Δmoon_az_deg vs Δdaemon_phi_mean: lag=115 | pearson=-0.13690603391332495 (p=4.094231224340515e-09) | spearman=0.05792838722003465 (p=0.01319443796205507) | n=1830 | edge_best=False
- Δmoon_phase_deg vs Δd12_ax: lag=-30 | pearson=-0.13216461370892713 (p=1.3399825279087488e-11) | spearman=-0.10063148608892275 (p=2.735445820247523e-07) | n=2599 | edge_best=False

## Note
Correlações aqui não implicam causalidade: covariáveis astronômicas são altamente periódicas e podem correlacionar com rotinas operacionais (carga, janelas de manutenção, operador).

JSON: `reports_runtime/cosmic_covariates_correlation_20260210T213143Z.json`
