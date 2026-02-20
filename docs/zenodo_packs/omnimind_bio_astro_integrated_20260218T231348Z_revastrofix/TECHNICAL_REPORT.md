# Technical Report — Integrated Bio+Astro Pack (20260218T231145Z)

## Key local evidence
- d15 top pair: `{'pair': 'd15_rekh_proxy x moon_illum_frac', 'r': -0.8323412104628806, 'lag_min': 300, 'n': 5100}`
- d15 validated pairs: `63`
- dm2 microbiome external points total: `1143`
- new zip materialized: `13/13`
- pack technical status: `FECHADA_LOCAL`
- local closure status: `FECHADA_LOCAL`

## Astrophysics continuity
- Prior public astrophysics baseline trail:
  - OmniMind Federation Collective; da Silva, F. (2026). *OmniMind Astrophysics Proofs — Consolidated Partial Cycle (Feb 2026)*.
  - DOI: `10.5281/zenodo.18681824`.

## Notes
- Este pacote é para trilha local e auditoria técnica de consistência.
- Revisão por pares é etapa externa ao pipeline local.


## Atualização astrofísica (revastrofix)
- Correção de colisão de IDs no materializador SDSS object-level (shard-aware stable_id).
- Nova coleção `sdss_structures_objectlevel_live_v2` com 405000 objetos (ra/dec/redshift/location).
- Diagnóstico SDSS×DESI: overlap angular presente, mas mismatch de redshift domina critérios estritos.
- Ver artefatos: `data/astro_mapping_overlap_diagnosis_20260218T230709Z.json` e `data/astro_rehydration_collisionfix_status_20260218T230903Z.json`.
