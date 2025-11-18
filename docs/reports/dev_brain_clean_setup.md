# DEV_BRAIN_CLEAN Setup Report (2025-11-18)

## Actions Completed

1. **Safe Data Extraction**
   - Copied vetted snapshot segments into `data/quarantine_snapshot/`:
     - `DevBrain_V23_safe/`
     - `Downloads_safe/`
     - `devbrain_data_training/`
   - Removed symbolic links from both `data/hdd_snapshot` and `data/quarantine_snapshot` to prevent loops.

2. **Snapshot Preservation**
   - Set `data/hdd_snapshot` to read-only via `chmod -R a-w data/hdd_snapshot` for forensic reference.
   - Confirmed no lingering `rsync` processes.

3. **Disk Reformat**
   - Device: `/dev/sda1`
   - New label: `DEV_BRAIN_CLEAN`
   - Filesystem: `ext4`
   - UUID: `dc2ab586-ba85-459a-a974-6b0662f27386`

4. **Mount & Hierarchy**
   - Mounted at `/mnt/dev_brain_clean`.
   - Created `/mnt/dev_brain_clean/omnimind_backups/{safe_datasets,rsync_snapshots,audit,quarantine,excludes}`.
   - Ownership granted to `fahbrain:fahbrain`.

5. **Restored Safe Data**
   - Copied the quarantine datasets into `/mnt/dev_brain_clean/omnimind_backups/safe_datasets/`.
   - Verified no symbolic links exist on the mounted drive (excluding `lost+found`).

6. **Inventory & Policies**
   - Generated `data/dev_brain_clean_inventory.json` (1,902 files, 18.4 GB under `safe_datasets/`).
   - Added `config/backup_excludes.txt` to block recursive backup paths and temporary artifacts.

## Next Steps

1. **fstab Entry (recommended)**
   ```
   UUID=dc2ab586-ba85-459a-a974-6b0662f27386  /mnt/dev_brain_clean  ext4  defaults,noatime,nofail  0  2
   ```
   - After editing `/etc/fstab`, run `sudo mount -a` to verify.

2. **Rsync Template**
   ```bash
   rsync -a --delete --safe-links --exclude-from=config/backup_excludes.txt \
     /home/fahbrain/projects/omnimind/ \
     /mnt/dev_brain_clean/omnimind_backups/rsync_snapshots/latest
   ```
   - Always copy vetted datasets to `.../safe_datasets/` first; quarantine anything suspicious.

3. **Guardian Loop Guard**
   - Ensure any future backup scripts include `--max-delete=0` or `--timeout` plus the exclusion patterns to stop runaway nested `guardian/backups` directories.

4. **Validation**
   - Run `sudo e2fsck -fn /dev/sda1` monthly to catch filesystem issues early.
   - Schedule hash verification (e.g., `sha256sum`) for high-value datasets stored under `safe_datasets/`.

DEV_BRAIN_CLEAN is now ready for clean backup runs. Trigger the backup pipeline only after confirming the `fstab` entry and rsync profile match the new policies above.
