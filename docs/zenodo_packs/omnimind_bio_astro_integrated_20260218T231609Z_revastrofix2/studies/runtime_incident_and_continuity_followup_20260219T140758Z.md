# Runtime Incident + Continuity Follow-up (20260219T140758Z)

- classification: `real-data-local`
- primary trigger: `systemd-oomd -> user dbus killed`
- session effect: `GNOME session reset/relogin (no full reboot)`

## Continuity
- phase2 progress: `FILE: /mnt/welinton_users/Public/datasets/zenodo_records/full_external/6797842/repo.zip`
- key processes: `aria2 + chain4 + qdrant + dream_weaver` active

## pCloud
- about: `{'total': 536870912000, 'used': 537511379424, 'free': 0}`
- top cleanup candidates:
  - `omnimind_offload`: `153.046 GiB` (objects `273`)
  - `DEV_BRAIN_CLEAN`: `85.24 GiB` (objects `113.139k (113139)`)
  - `omnimind_memory`: `30.706 GiB` (objects `4.777k (4777)`)
  - `omnimind_cold`: `16.637 GiB` (objects `113`)
  - `omnimind_archives`: `5.613 GiB` (objects `127`)

## Root archives ingestion
- materialized: `5` / `5`
  - `astro_brown_dwarfs_photometric_17684859_live`: entries=`1`, rows=`0`, points=`2`
  - `astro_gmos_gri_fits_56059_live`: entries=`17`, rows=`0`, points=`136`
  - `bio_gemini_multimorbidity_ltc_14824760_live`: entries=`1`, rows=`0`, points=`90`
  - `astro_extrasolar_asteroid_transits_1317527_live`: entries=`1`, rows=`0`, points=`1`
  - `chem_tandem_mass_spectra_llm_17555571_live`: entries=`13`, rows=`30138`, points=`30157`

JSON: `/home/fahbrain/projects/omnimind/reports_runtime/runtime_incident_and_continuity_followup_20260219T140758Z.json`
