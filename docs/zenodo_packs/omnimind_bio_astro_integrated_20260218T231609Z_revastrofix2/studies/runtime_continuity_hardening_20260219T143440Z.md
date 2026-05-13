# Runtime Continuity + Hardening (20260219T143440Z)

- classification: `real-data-local`

## Incident Root Cause
- primary: `Feb 19 11:33:42 omnimind-dev systemd[1]: Started Userspace Out-Of-Memory (OOM) Killer.`
- conclusion: memory-pressure cascade in user session; NVIDIA lines are secondary in restart path.

## Hardening Applied
- swappiness: `65`
- vfs_cache_pressure: `80`
- oomd drop-in: `/etc/systemd/oomd.conf.d/99-omnimind-antireset.conf`

## Wellington Download
- file: `/mnt/welinton_users/Public/datasets/zenodo_records/full_external/6797842/repo.zip`
- exists: `True` size_bytes=`24780453704`
- phase2 status: `completed`

## pCloud
- total: `536870912000`
- used: `459008115898`
- free: `77862796102`
- snapshots_autonomous_loop count: `137` bytes=`85828427781`

JSON: `/home/fahbrain/projects/omnimind/reports_runtime/runtime_continuity_hardening_20260219T143440Z.json`
