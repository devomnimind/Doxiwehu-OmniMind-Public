# Aging Studies Refinement (Real-data) 20260219T124425Z

- source_json: `/home/fahbrain/projects/omnimind/reports_runtime/aging_studies_refinement_realdata_20260219T124425Z.json`
- rows_used: `44581`
- hotspot_cluster_id: `3`

## Orthogonalization check
- moon_to_mitophagy_r2: `0.9994326249233785`
- raw mitophagy vs senescence r: `-0.3411756832509929`
- orthogonal mitophagy vs senescence r: `0.019303711597662795`
- orthogonal mitophagy vs senescence p: `4.5798844197591265e-05`

## Granger (lag 1..10)
- min p (mitophagy_orth -> senescence): `0.0045326952722676795`
- min p (senescence -> mitophagy_orth): `2.0475051989200816e-81`

## D12/D15 hotspot fractions (top5)
- house12 top: `[{'house_d12': 12, 'hotspot_fraction': 0.4962585647313379}, {'house_d12': 1, 'hotspot_fraction': 0.08402911104165736}]`
- sector15 top: `[{'sector_d15': 15, 'hotspot_fraction': 0.4962585647313379}, {'sector_d15': 1, 'hotspot_fraction': 0.08402911104165736}]`

## Disease collection scan readiness
- scanned_collections: `7`
- note: sampled payloads currently do not expose direct `house_d12`/`sector_d15` keys in the scanned disease collections; cross-assignment must be done by temporal/phase join or added payload schema.
