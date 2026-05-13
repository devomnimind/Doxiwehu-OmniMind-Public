# Orbit Queue Trails (20260211T0149Z)

Artefatos gerados a partir de:
- `reports_runtime/orbit_queue_dodecatiad_20260210T024651Z.json` (janela 2026-02-10→2026-02-11, step=0.5h)
- Métricas internas: `sinthome_13`, `sinthome_quadruple`
- Enriquecimento físico (quando disponível): `reports_runtime/sbdb_physical_20260210T224704Z.json` (JPL SBDB)

## Imagens (3D/4D)
- `orbit_queue_trails_3d_20260211T014910Z.png`
  - Linhas 3D: RA (desenrolado), Dec, tempo (h desde o início da janela).
- `orbit_queue_trails_4d_sinthome13_20260211T014910Z.png`
  - Nuvem 3D com cor = `sinthome_13` (1 - cosine 12D).
- `orbit_queue_trails_4d_sinthome_quadruple_20260211T014910Z.png`
  - Nuvem 3D com cor = `sinthome_quadruple` (1 - cosine (Φ,Ψ,σ,ε)).

## Camada Física (SBDB)
As imagens físicas só são renderizadas quando existem pontos suficientes com valores conhecidos no SBDB.

- `orbit_queue_trails_4d_sbdb_K1_20260211T014928Z.png`
- `orbit_queue_trails_4d_sbdb_M1_20260211T014928Z.png`
- `orbit_queue_trails_4d_sbdb_M2_20260211T014928Z.png`

## Sumários
- `orbit_queue_trails_summary_20260211T014910Z.json`
- `orbit_queue_trails_physical_summary_20260211T014928Z.json`

