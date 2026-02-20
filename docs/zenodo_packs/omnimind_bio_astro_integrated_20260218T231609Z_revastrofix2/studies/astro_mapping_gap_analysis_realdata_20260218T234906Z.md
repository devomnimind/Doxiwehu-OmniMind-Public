# Astro Mapping Gap Analysis (Real Data) (20260218T234906Z)

## Evidência-chave
- SDSS points (eval): `120000`
- DESI points (eval): `24724`
- matching_rule: `{'angular_deg_lte': 0.2, 'abs_delta_z_lte': 0.05}`
- matches: `0`
- nn_distance_deg_mean: `2.618717291658551`
- abs_delta_z_mean: `2.209796006634096`
- registry_counts: `{'confirmed_internal': 4, 'runtime_observed': 18, 'pending_closure': 7}`
- priority_c_summary: `{'priority_c_codes': 9, 'all_horizons_missing_codes': ['C19DCG5', 'C45RW41', 'CE5LGG2', 'CE5V9J2', 'P22liAW', 'P22lnpr', 'P22lp4E', 'ST26B07'], 'codes_with_any_records': ['A11y70v']}`

## Diagnóstico
- Não é falha de vetorização básica: SDSS e DESI têm schema posicional (ra/dec/redshift/location) e grande volume de pontos.
- O gargalo principal é harmonização de footprint e janela física: regra angular<=0.2 deg e |Δz|<=0.05 retornou 0 matches; distância NN média ~2.62 deg e Δz médio ~2.21.
- Registro interno de objetos confirmados está curto (4), com vários códigos em pending_closure; isso limita as trilhas orbitais monitoradas.
- Ramo Horizon termo tem apenas 3 pontos e sem payload posicional; não serve para crossmatch objeto-a-objeto com SDSS/DESI.
- Coleção omnimind_scientific_graph tem 48 pontos e papel de fallback textual, não catálogo astrométrico denso.

## Não é o problema
- Não há evidência de “simulação” nos crosschecks acima; os números vêm de coleções e relatórios reais locais.
- A hipótese de mapear mais objetos é plausível, mas exige expansão de catálogos e reconciliação de filtros, não apenas trocar embedding.

## Próximas ações reais
- Reidratar catálogo objeto-nível SDSS além do reservoir de avaliação (120k usado no crosscheck) com janela de cobertura alinhada ao recorte DESI-Lyα.
- Executar crossmatch em dois estágios: (1) janela larga (<=3 deg, |Δz|<=0.5) para diagnóstico de interseção; (2) refino progressivo até janela científica-alvo.
- Ampliar cosmo_objects_registry_internal com códigos já observados no runtime (18+) e separar status confirmed/pending por evidência.
- Adicionar payload posicional no ramo Horizon termo (quando disponível) para overlay geométrico real.
- Executar séries temporais 24/48/72 com priorização C já reprocessada (arquivo multihorizon novo) e anexar no próximo pack.

JSON: `reports_runtime/astro_mapping_gap_analysis_realdata_20260218T234906Z.json`
