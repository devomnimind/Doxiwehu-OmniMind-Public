# External HDD Dataset Inventory (2025-11-18)

## Scope

Systematically crawled `/run/media/fahbrain/DevBrain_Storage` to locate every `*.jsonl` dataset present on the external drive. Results cover 2,080 artifacts and are stored for traceability in:

- `data/external_drive_inventory.json` → full per-file metadata (path, size, mtime).
- `data/external_drive_inventory_summary.json` → aggregated view by top-level folder.

Only discovery and classification were performed. **No files were copied or imported into OmniMind.**

## High-Level Totals

| Top-Level Folder | File Count | Approx. Size |
| --- | ---: | ---: |
| `QUARENTENA_DEVBRAIN_V1` | 1,795 | 8.61 GB |
| `Quarentena` | 276 | 1.31 GB |
| `DOwnlods bakup` | 7 | 1.11 GB |
| `DevBrain_V23` | 2 | < 10 MB |
| `devbrain_archive` | **Permission denied** | n/a |

> Note: Remaining top-level folders either contained no JSONL datasets or required elevated permissions. `devbrain_archive` threw repeated `PermissionError`; keep it isolated until a forensics-approved mount is available.

## Notable Collections (Sampled Entries)

### `QUARENTENA_DEVBRAIN_V1`
- Multiple nested `guardian/backups` snapshots (daily chain) bundling:
  - `data/training_v18/training_dataset.jsonl` (~20 MB each)
  - `monitoring/activity_*.jsonl` (0.9–13 MB per day)
  - `archived_intents/*.jsonl` (~5 MB) and `cog_layer/{decisions,reflections}.jsonl`
- Legacy orchestrator artifacts under `src/ai-orchestrator-content/data/*` (0.1–9 MB) including `global_training_data.jsonl` and `personality/decisions.jsonl`.
- High-risk telemetry such as `devbrain/v14/monitoring/metrics_20251110.jsonl` (8.3 MB) and `notifications.jsonl` (3 MB).

**Risk Tag:** `Quarantine-Critical`. These files originated from compromised deployments, so they stay isolated until malware scanning + schema validation are complete.

### `Quarentena`
- Rotating monitoring datasets (`activity_YYYYMMDD.jsonl`) and `decision_stream.jsonl` taken from pre-RLAIF builds.
- Incremental `self-healing` logs (50–150 KB) that may still reference deprecated APIs.

**Risk Tag:** `Quarantine-Moderate`. Structure appears stable, but provenance remains unclear. Requires static malware scan plus content sampler before reuse.

### `DOwnlods bakup`
- `devbrain_data/training/devbrain_training_data.jsonl` (~1.1 GB) – appears to be a consolidated intent/action corpus.
- Full incremental bundle `devbrain_complete_consolidated.jsonl` (~2 MB) with auditing context.

**Risk Tag:** `Candidate-Safe` pending checksum verification. This directory was copied prior to the corruption incident and showed no suspicious timestamps.

### `DevBrain_V23`
- Only two lightweight JSONL stubs (`session_manifest.jsonl`, `session_metrics.jsonl`).

**Risk Tag:** `Candidate-Safe`. Still needs schema diff vs. Phase 6 expectations.

## Recommended Next Steps

1. **Immutable Snapshot:** Use `rsync --archive --numeric-ids --exclude 'devbrain_archive'` to copy the current layout into a read-only evidence folder before touching any files.
2. **Forensic Scans:**
   - Run `clamdscan` and `rkhunter --check` on `QUARENTENA_DEVBRAIN_V1` and `Quarentena` before mounting read/write.
   - Validate JSONL schema via a streaming parser to detect truncated/poisoned records.
3. **Prioritized Imports:**
   - Start with small `DevBrain_V23` and `DOwnlods bakup` corpora once scans pass.
   - Hold all `guardian/backups` bundles until the SecurityAgent playbooks approve them.
4. **Tooling Tie-In:** Feed `data/external_drive_inventory.json` into the upcoming External HDD analysis utility to auto-score integrity, hash chains, and sampling stats.

## Pending Work

- [ ] Add SHA-256 hashing stage per file (deferred to the analysis tool to avoid double I/O today).
- [ ] Attempt controlled access to `devbrain_archive` when safe credentials are available.
- [ ] Merge safe datasets into the Hugging Face sync plan only after completing security validation.

This report satisfies the requested “catalog first” directive. Confirm when it is safe to escalate individual datasets for import or sanitization.
