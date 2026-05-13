# Offload Cold Guardrail Check (20260211T180128Z)

## Updated scripts
- `scripts/maintenance/offload_to_smb_symlink.sh`
- `scripts/maintenance/offload_file_to_smb_symlink.sh`

## New flags
- `--check-only`
- `--cold-window-min`
- `--allow-hot` (exception only)

## Validation checks
- `OMNIMIND_SOMA_EXPANSION`: blocked (recent write detected: `monitor/gadget_cache.json`)
- `Sovereign_Backup_1768407190.omni`: passed (cold-data preflight)

JSON: `reports_runtime/offload_cold_guardrail_check_20260211T180128Z.json`
