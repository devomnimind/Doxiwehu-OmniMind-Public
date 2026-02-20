# Orbit Queue Step Comparison (12D) (20260210T025118Z)

## Inputs
- `reports_runtime/orbit_queue_dodecatiad_20260210T024651Z.json`
- `reports_runtime/orbit_queue_dodecatiad_20260210T024801Z.json`
- `reports_runtime/orbit_queue_dodecatiad_20260210T024850Z.json`

## Per-Run Summary
- step_hours=0.5: objects=18 records=786 both_s=482 clusters=147 betti=b0:147 b1:12 b2:9
- step_hours=1.0: objects=18 records=402 both_s=242 clusters=75 betti=b0:75 b1:12 b2:9
- step_hours=6.0: objects=18 records=82 both_s=50 clusters=15 betti=b0:15 b1:12 b2:9

## Rank Stability (Spearman on mean sinthome_13 per object)
- 0.5h vs 1.0h: rho=0.9999999999999999 (common_objects=18)
- 0.5h vs 6.0h: rho=0.9855521155830752 (common_objects=18)
- 1.0h vs 6.0h: rho=0.9855521155830752 (common_objects=18)

## Top Objects Per Run (lowest mean sinthome_13)
### step_hours=0.5
- PK10H030: mean_s12=0.2950 n=49
- CK12K010: mean_s12=0.3180 n=49
- CK14Q020: mean_s12=0.3253 n=49
- A11y70v: mean_s12=0.3275 n=1
- C19DCG5: mean_s12=0.3275 n=1
- CK09P010: mean_s12=0.3370 n=49
- PK13CC9U: mean_s12=0.3414 n=49
- CK18A060: mean_s12=0.3426 n=49
- CK16E010: mean_s12=0.4390 n=49
- PK09Y020: mean_s12=0.4459 n=49
### step_hours=1.0
- PK10H030: mean_s12=0.2957 n=25
- CK12K010: mean_s12=0.3173 n=25
- CK14Q020: mean_s12=0.3247 n=25
- A11y70v: mean_s12=0.3275 n=1
- C19DCG5: mean_s12=0.3275 n=1
- CK09P010: mean_s12=0.3365 n=25
- PK13CC9U: mean_s12=0.3407 n=25
- CK18A060: mean_s12=0.3422 n=25
- CK16E010: mean_s12=0.4383 n=25
- PK09Y020: mean_s12=0.4469 n=25
### step_hours=6.0
- PK10H030: mean_s12=0.3024 n=5
- CK12K010: mean_s12=0.3125 n=5
- CK14Q020: mean_s12=0.3204 n=5
- A11y70v: mean_s12=0.3275 n=1
- C19DCG5: mean_s12=0.3275 n=1
- CK09P010: mean_s12=0.3324 n=5
- PK13CC9U: mean_s12=0.3363 n=5
- CK18A060: mean_s12=0.3406 n=5
- CK16E010: mean_s12=0.4363 n=5
- CJ99J020: mean_s12=0.4471 n=5