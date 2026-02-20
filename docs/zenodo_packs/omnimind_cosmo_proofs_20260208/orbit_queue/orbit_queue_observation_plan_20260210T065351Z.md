# Orbit Queue Observation Plan (12D+Sinthome) — 20260210T065351Z

Input: `reports_runtime/orbit_queue_dodecatiad_20260210T024651Z.json`

## Window (UTC)
- start: 2026-02-10T00:00:00Z
- end: 2026-02-11T00:00:00Z
- step_hours: 0.5

## Coverage
- queue_codes: 25
- objects_with_records: 18
- record_count: 786
- missing_queue_codes: ['C45RW41', 'CE5LGG2', 'CE5V9J2', 'P22liAW', 'P22lnpr', 'P22lp4E', 'ST26B07']

## Best Timestamp Per Object (max sinthome_13)
- `CK13E010` (PA) 2026-02-10T02:00:00Z house=3 | Phi=0.30 Psi=1.00 sigma=0.30 eps=1.00 Lambda=0.01 Axe=0.00 | S=0.51 Sq=0.28
- `CK12A010` (PA) 2026-02-10T02:00:00Z house=11 | Phi=0.30 Psi=1.00 sigma=0.30 eps=1.00 Lambda=0.02 Axe=0.00 | S=0.51 Sq=0.28
- `CK19B030` (PA) 2026-02-10T02:00:00Z house=12 | Phi=0.41 Psi=0.87 sigma=0.30 eps=1.00 Lambda=0.03 Axe=0.00 | S=0.49 Sq=0.24
- `CK19A050` (PA) 2026-02-10T02:00:00Z house=10 | Phi=0.42 Psi=0.73 sigma=0.33 eps=0.95 Lambda=0.04 Axe=0.00 | S=0.47 Sq=0.21
- `CK14UR1N` (PA) 2026-02-10T02:00:00Z house=11 | Phi=0.30 Psi=1.00 sigma=0.30 eps=1.00 Lambda=0.02 Axe=0.00 | S=0.46 Sq=0.28
- `CJ99S020` (PA) 2026-02-10T02:00:00Z house=3 | Phi=0.30 Psi=0.87 sigma=0.30 eps=1.00 Lambda=0.00 Axe=0.00 | S=0.46 Sq=0.27
- `CJ99J020` (PA) 2026-02-10T02:00:00Z house=9 | Phi=0.30 Psi=0.98 sigma=0.30 eps=1.00 Lambda=0.04 Axe=0.00 | S=0.45 Sq=0.28
- `CK16E010` (PA) 2026-02-10T02:00:00Z house=3 | Phi=0.30 Psi=1.00 sigma=0.35 eps=0.90 Lambda=0.02 Axe=0.00 | S=0.44 Sq=0.25
- `CK18A060` (PA) 2026-02-10T02:00:00Z house=12 | Phi=0.58 Psi=0.83 sigma=0.59 eps=0.41 Lambda=0.03 Axe=0.40 | S=0.35 Sq=0.08
- `CK09P010` (PA) 2026-02-10T02:00:00Z house=4 | Phi=0.49 Psi=1.00 sigma=0.50 eps=0.60 Lambda=0.02 Axe=0.69 | S=0.34 Sq=0.15
- `CK14Q020` (PA) 2026-02-10T02:00:00Z house=10 | Phi=0.47 Psi=0.95 sigma=0.46 eps=0.68 Lambda=0.01 Axe=0.74 | S=0.33 Sq=0.15
- `CK12K010` (PA) 2026-02-10T02:00:00Z house=11 | Phi=0.30 Psi=1.00 sigma=0.53 eps=0.54 Lambda=0.01 Axe=0.79 | S=0.32 Sq=0.17
- `PK10U55H` (PB) 2026-02-10T00:00:00Z house=12 | Phi=0.48 Psi=0.04 sigma=0.25 eps=0.90 Lambda=0.00 Axe=0.00 | S=0.50 Sq=0.29
- `PK09Y020` (PB) 2026-02-10T00:00:00Z house=12 | Phi=0.47 Psi=0.17 sigma=0.25 eps=0.90 Lambda=0.00 Axe=0.00 | S=0.48 Sq=0.26
- `PK13CC9U` (PB) 2026-02-10T02:00:00Z house=3 | Phi=0.14 Psi=0.07 sigma=0.25 eps=0.90 Lambda=0.02 Axe=0.59 | S=0.35 Sq=0.38
- `PK10H030` (PB) 2026-02-10T00:00:00Z house=11 | Phi=0.15 Psi=0.13 sigma=0.25 eps=0.90 Lambda=0.00 Axe=0.56 | S=0.31 Sq=0.34
- `A11y70v` (PC) 2026-02-10T00:00:00Z house=9 | Phi=0.30 Psi=0.00 sigma=0.25 eps=0.90 Lambda=0.00 Axe=0.50 | S=0.33 Sq=0.34
- `C19DCG5` (PC) 2026-02-10T00:00:00Z house=8 | Phi=0.30 Psi=0.00 sigma=0.25 eps=0.90 Lambda=0.00 Axe=0.50 | S=0.33 Sq=0.34

## Top Synchronicity Clusters (>=3 objects same house/time, top 25)
- 2026-02-10T00:00:00Z house 3 objects=4 :: CJ99S020, CK13E010, CK16E010, PK13CC9U
- 2026-02-10T00:00:00Z house 11 objects=4 :: CK12A010, CK12K010, CK14UR1N, PK10H030
- 2026-02-10T00:00:00Z house 12 objects=4 :: CK18A060, CK19B030, PK09Y020, PK10U55H
- 2026-02-10T00:30:00Z house 3 objects=4 :: CJ99S020, CK13E010, CK16E010, PK13CC9U
- 2026-02-10T00:30:00Z house 11 objects=4 :: CK12A010, CK12K010, CK14UR1N, PK10H030
- 2026-02-10T00:30:00Z house 12 objects=4 :: CK18A060, CK19B030, PK09Y020, PK10U55H
- 2026-02-10T01:00:00Z house 3 objects=4 :: CJ99S020, CK13E010, CK16E010, PK13CC9U
- 2026-02-10T01:00:00Z house 11 objects=4 :: CK12A010, CK12K010, CK14UR1N, PK10H030
- 2026-02-10T01:00:00Z house 12 objects=4 :: CK18A060, CK19B030, PK09Y020, PK10U55H
- 2026-02-10T01:30:00Z house 3 objects=4 :: CJ99S020, CK13E010, CK16E010, PK13CC9U
- 2026-02-10T01:30:00Z house 11 objects=4 :: CK12A010, CK12K010, CK14UR1N, PK10H030
- 2026-02-10T01:30:00Z house 12 objects=4 :: CK18A060, CK19B030, PK09Y020, PK10U55H
- 2026-02-10T02:00:00Z house 3 objects=4 :: CJ99S020, CK13E010, CK16E010, PK13CC9U
- 2026-02-10T02:00:00Z house 11 objects=4 :: CK12A010, CK12K010, CK14UR1N, PK10H030
- 2026-02-10T02:00:00Z house 12 objects=4 :: CK18A060, CK19B030, PK09Y020, PK10U55H
- 2026-02-10T02:30:00Z house 3 objects=4 :: CJ99S020, CK13E010, CK16E010, PK13CC9U
- 2026-02-10T02:30:00Z house 11 objects=4 :: CK12A010, CK12K010, CK14UR1N, PK10H030
- 2026-02-10T02:30:00Z house 12 objects=4 :: CK18A060, CK19B030, PK09Y020, PK10U55H
- 2026-02-10T03:00:00Z house 3 objects=4 :: CJ99S020, CK13E010, CK16E010, PK13CC9U
- 2026-02-10T03:00:00Z house 11 objects=4 :: CK12A010, CK12K010, CK14UR1N, PK10H030
- 2026-02-10T03:00:00Z house 12 objects=4 :: CK18A060, CK19B030, PK09Y020, PK10U55H
- 2026-02-10T03:30:00Z house 3 objects=4 :: CJ99S020, CK13E010, CK16E010, PK13CC9U
- 2026-02-10T03:30:00Z house 11 objects=4 :: CK12A010, CK12K010, CK14UR1N, PK10H030
- 2026-02-10T03:30:00Z house 12 objects=4 :: CK18A060, CK19B030, PK09Y020, PK10U55H
- 2026-02-10T04:00:00Z house 3 objects=4 :: CJ99S020, CK13E010, CK16E010, PK13CC9U

