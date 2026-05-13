# Gaia Download Status (20260208T213937Z)

- Wanted files: **40**
- Present (`*.csv.gz`): **49**
- Missing from target list: **0**
- Size: `10G	/home/fahbrain/projects/omnimind/data/gaia_bulk/gaia_source`
- Latest log: `/home/fahbrain/projects/omnimind/data/gaia_bulk/gaia_resume_detached_20260208T213237Z.log`

## Missing files

## Extra files (not in list)
- `GaiaSource_000000-003111.csv.gz`
- `GaiaSource_003112-005263.csv.gz`
- `GaiaSource_005264-006601.csv.gz`
- `GaiaSource_006602-007952.csv.gz`
- `GaiaSource_007953-010234.csv.gz`
- `GaiaSource_010235-012597.csv.gz`
- `GaiaSource_012598-014045.csv.gz`
- `GaiaSource_015370-016240.csv.gz`
- `GaiaSource_016241-017018.csv.gz`

## Active download processes
- `3497011 /bin/bash -c . "/home/fahbrain/.codex/shell_snapshots/019c3126-cb2b-7951-a8cb-c6bca45e8980.sh" && cd /home/fahbrain/projects/omnimind && .venv/bin/python - <<'PY' from pathlib import Path from datetime import datetime, timezone import json, subprocess  root=Path('/home/fahbrain/projects/omnimind') list_path=root/'data/gaia_bulk/gaia_download_list_20260208.txt' source_dir=root/'data/gaia_bulk/gaia_source' ts=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') want=[l.strip() for l in list_path.read_text().splitlines() if l.strip()] have={p.name for p in source_dir.glob('*.csv.gz')} missing=[w for w in want if w not in have] extra=sorted([h for h in have if h not in set(want)]) proc=subprocess.run("pgrep -af 'resume_gaia_missing.sh|wget -4 -c --timeout=30 --tries=3'", shell=True, capture_output=True, text=True) log_files=sorted((root/'data/gaia_bulk').glob('gaia_resume_detached_*.log')) latest_log=str(log_files[-1]) if log_files else None summary={   'timestamp': ts,   'wanted_files': len(want),   'have_total_csv_gz': len(have),   'missing_from_target_list': len(missing),   'missing_files': missing,   'extra_files_not_in_target_list': extra,   'source_dir': str(source_dir),   'size_human': subprocess.run(f"du -sh {source_dir}", shell=True, capture_output=True, text=True).stdout.strip(),   'download_processes': [l for l in proc.stdout.splitlines() if l.strip()],   'latest_log': latest_log, } out_json=root/f'data/reports/gaia_download_status_{ts}.json' out_md=root/f'data/reports/gaia_download_status_{ts}.md' out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8') md=[f"# Gaia Download Status ({ts})", "", f"- Wanted files: **{len(want)}**", f"- Present (`*.csv.gz`): **{len(have)}**", f"- Missing from target list: **{len(missing)}**", f"- Size: `{summary['size_human']}`", f"- Latest log: `{latest_log}`", "", "## Missing files"] for m in missing:     md.append(f"- `{m}`") if extra:     md += ["", "## Extra files (not in list)"]     for e in extra:         md.append(f"- `{e}`") md += ["", "## Active download processes"] if summary['download_processes']:     for p in summary['download_processes']:         md.append(f"- `{p}`") else:     md.append("- none") out_md.write_text('\n'.join(md)+'\n', encoding='utf-8') print(out_json) print(out_md) PY`
- `3497013 /bin/sh -c pgrep -af 'resume_gaia_missing.sh|wget -4 -c --timeout=30 --tries=3'`
