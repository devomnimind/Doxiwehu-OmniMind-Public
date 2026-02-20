# Orbit Mapping Next Actions (20260209T230703Z)

## Summary
- high_i_candidates: 12
- resonance_candidates: 4
- no_orbit_candidates: 9

## Priority A — High-i + Low D_SH
- CK18A060: i=77.190°, D_SH=0.414, ref=K18P28L, e=0.798939
- CK12K010: i=142.596°, D_SH=0.543, ref=K19E03J, e=0.999871
- CK09P010: i=106.224°, D_SH=0.602, ref=K17O68X, e=0.999850
- CK14Q020: i=80.794°, D_SH=0.676, ref=K17Y03N, e=0.996800
- CK16E010: i=131.871°, D_SH=0.898, ref=p7717, e=1.001501
- CK19A050: i=67.555°, D_SH=0.947, ref=Y2842, e=0.706658
- CK19B030: i=66.627°, D_SH=0.998, ref=w4778, e=0.997820
- CK12A010: i=121.009°, D_SH=1.060, ref=K25M88U, e=0.999707
- CK14UR1N: i=95.446°, D_SH=1.202, ref=q3800, e=1.004321
- CJ99S020: i=65.634°, D_SH=1.464, ref=K24P38P, e=1.002279
- CJ99J020: i=86.402°, D_SH=1.485, ref=K25M88U, e=1.000772
- CK13E010: i=158.711°, D_SH=1.643, ref=K25M88U, e=0.998824

## Priority B — Resonance Watch (Jupiter)
- PK09Y020: ratio=1.408 (7:5)
- PK10H030: ratio=0.446 (3:7)
- PK10U55H: ratio=1.444 (7:5)
- PK13CC9U: ratio=0.417 (3:7)

## Priority C — No-orbit closure (top IDs)
- A11y70v
- C19DCG5
- C45RW41
- CE5LGG2
- CE5V9J2
- P22liAW
- P22lnpr
- P22lp4E
- ST26B07

## Recommended Queue
- queue_A_followup_ephemerides: track high_i_low_d objects in next 24h windows with real RA/Dec, delta-arc >= 2 nights
- queue_B_resonance_watch: monitor Jupiter 7:5 and 3:7 regimes in candidates list
- queue_C_no_orbit_resolution: prioritize NEOCP-only IDs for orbit closure using multi-epoch tracklets
- queue_D_house_overlay: overlay queue A/B objects on Dodecatiade houses and compare with satellite masks

JSON: `reports_runtime/orbit_mapping_next_actions_20260209T230703Z.json`
