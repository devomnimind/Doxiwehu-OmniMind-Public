# Offload Progress (20260211T033852Z)

## Disk
- /: /dev/nvme0n1p2  366G  328G   20G  95% /
- /var: /dev/nvme0n1p5  247G  228G  6.2G  98% /var
- /home: /dev/nvme0n1p3  274G  253G  7.8G  98% /home
- /mnt/welinton_users: //192.168.15.5/Users  466G  129G  337G  28% /mnt/welinton_users

## Paths
- /omnimind_storage/offload_var/backups/sovereign_images/omnimind_image_1767157461 (symlink -> /var/omnimind_storage/home_redirect/offload_root/backup_migration_20260211/omnimind_image_1767157461)
- /omnimind_storage/offload_var/backups/sovereign_images/omnimind_image_1767380192 (exists)
- /var/omnimind_storage/home_redirect/offload_root/backup_migration_20260211/omnimind_image_1767157461 (exists)
- /mnt/welinton_users/Public/datasets/omnimind_offload2_20260211/omnimind_image_1767380192 (missing/unreachable)

## Processes
- 3257997 rsync -a /omnimind_storage/offload_var/backups/sovereign_images/omnimind_image_1767380192/ /mnt/welinton_users/Public/datasets/omnimind_offload2_20260211/omnimind_image_1767380192/
- 3257998 rsync -a /omnimind_storage/offload_var/backups/sovereign_images/omnimind_image_1767380192/ /mnt/welinton_users/Public/datasets/omnimind_offload2_20260211/omnimind_image_1767380192/
- 3257999 rsync -a /omnimind_storage/offload_var/backups/sovereign_images/omnimind_image_1767380192/ /mnt/welinton_users/Public/datasets/omnimind_offload2_20260211/omnimind_image_1767380192/
- 3271554 bash -lc cd /home/fahbrain/projects/omnimind TS=$(date -u +%Y%m%dT%H%M%SZ) OUT_DIR="docs/zenodo_packs/omnimind_cosmo_proofs_20260208/storage_ops/$TS" mkdir -p "$OUT_DIR" {   echo "# Offload Progress ($TS)"   echo   echo "## Disk"   echo "- /: $(df -h / | tail -n 1)"   echo "- /var: $(df -h /var | tail -n 1)"   echo "- /home: $(df -h /home | tail -n 1)"   echo "- /mnt/welinton_users: $(df -h /mnt/welinton_users | tail -n 1)"   echo   echo "## Paths"   for p in \    /omnimind_storage/offload_var/backups/sovereign_images/omnimind_image_1767157461 \    /omnimind_storage/offload_var/backups/sovereign_images/omnimind_image_1767380192 \    /var/omnimind_storage/home_redirect/offload_root/backup_migration_20260211/omnimind_image_1767157461 \    /mnt/welinton_users/Public/datasets/omnimind_offload2_20260211/omnimind_image_1767380192 ; do     if timeout 5 test -L "$p"; then       echo "- $p (symlink -> $(readlink -f "$p"))"     elif timeout 5 test -e "$p"; then       echo "- $p (exists)"     else       echo "- $p (missing/unreachable)"     fi   done   echo   echo "## Processes"   pgrep -af "omnimind_image_1767380192/ /mnt/welinton_users/Public/datasets/omnimind_offload2_20260211" | sed "s/^/- /" || echo "- none" } > "$OUT_DIR/offload_progress_${TS}.md" cat > "$OUT_DIR/offload_progress_${TS}.json" <<JSON {   "timestamp": "$TS",   "md": "storage_ops/$TS/offload_progress_${TS}.md" } JSON printf "%s\n%s\n" "$OUT_DIR/offload_progress_${TS}.json" "$OUT_DIR/offload_progress_${TS}.md"
