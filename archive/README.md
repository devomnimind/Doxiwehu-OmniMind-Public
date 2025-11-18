# Archive Watchlist

This directory collects retired artifacts, reference demos, and documentation snapshots that were moved out of the root to keep the main workspace clean.

## Subdirectories

- `archive/examples/` – Contained legacy demo scripts (`demo_phase6*.py`) plus the CUDA experiment folder now located in `archive/examples/cuda/`.
- `archive/reports/` – Stores the Phase 6/7 reports and status exports (`RELATORIO_*`, `RESUMO_EXECUTIVO_PHASE6.md`, `STATUS_PROJECT.md`, `INDEX.md`). These files are for historical reference only.

**NOTE:** These contents are preserved for traceability and SHOULD NOT be executed as part of the main CI/CD pipeline unless explicitly needed. Keep modifications minimal and document the reason for editing any archived file.