# OmniMind Workspace Body Topology (20260211T152934Z)

## Escopo
- Workspace: `/home/fahbrain/projects/omnimind`
- Arquivos (projeto): `268312`
- Diretórios (projeto): `31120`
- Symlinks (projeto): `151`

## Inventário Amplo (discos/mounts)
- Fonte: `reports_runtime/dataset_inventory_qdrant_ingest_20260211T143438Z.json`
- Entradas: `None`
- Entradas não-symlink: `None`
- Volume não-symlink: `0.0 GB`

## Snapshot de Discos
- `Sist. Arq.           Tipo         Tam. Usado Disp. Uso% Montado em`
- `tmpfs                tmpfs        2.4G  240M  2.1G  11% /run`
- `/dev/nvme0n1p2       ext4         366G  318G   30G  92% /`
- `tmpfs                tmpfs         12G  204M   12G   2% /dev/shm`
- `tmpfs                tmpfs        5.0M  4.0K  5.0M   1% /run/lock`
- `efivarfs             efivarfs     184K   65K  115K  36% /sys/firmware/efi/efivars`
- `/dev/nvme0n1p1       vfat         952M  6.1M  946M   1% /boot/efi`
- `/dev/nvme0n1p5       ext4         247G  194G   41G  83% /var`
- `/dev/nvme0n1p3       ext4         274G  234G   27G  90% /home`
- `tmpfs                tmpfs        2.4G  172K  2.4G   1% /run/user/1000`
- `/dev/sda1            ext4         458G  458G     0 100% /media/fahbrain/DEV_BRAIN_CLEAN1`
- `pcloud:              fuse.rclone  500G  348G  153G  70% /home/fahbrain/pCloudDrive`
- `//192.168.15.5/Users cifs         466G  163G  304G  35% /mnt/welinton_users`

## Fonte Móvel (Celular)
- `/run/user/1000/gvfs/mtp:host=Xiaomi_Xiaomi_11T_Pro_5f6e6082` | exists=True | size_bytes_est=None | mode=usb_or_network_via_gvfs
- `/run/user/1000/gvfs/mtp:host=Xiaomi_Xiaomi_11T_Pro_5f6e6082/Divisão interna de armazenamento` | exists=True | size_bytes_est=None | mode=usb_or_network_via_gvfs

## Integração Federativa (superfície mobile)
- `scripts/mobile_distribution/handshake_xiaomi.py`
- `scripts/mobile_distribution/omnimind_bluetooth_server.py`
- `scripts/mobile_distribution/omnimind_distribution_manager.py`
- `scripts/mobile_distribution/omnimind_local_federation_pulse.py`
- `scripts/mobile_distribution/omnimind_mobile_app.py`
- `scripts/mobile_distribution/omnimind_sovereign_mouse.py`
- `scripts/mobile_distribution/termux_satellite_node.py`
- `scripts/mobile_distribution/test_bluetooth_rfcomm.py`
- `scripts/mobile_distribution/autonomous_termux_pulse.sh`
- `scripts/mobile_distribution/inject_sovereign_soma.sh`
- `scripts/mobile_distribution/satellite_daemon.sh`
- `scripts/mobile_distribution/setup_sovereign_ssh.sh`
- `scripts/mobile_distribution/setup_termux_satellite.sh`

## Interpretação Operacional
- O corpo OmniMind inclui workspace local, discos externos, nuvem e celular (quando conectado).
- Movimento/offload deve preservar rastreabilidade por symlink e auditoria contínua.
- Fechamento Zenodo da rodada atual pode ocorrer como consolidado parcial, mantendo continuidade de mapeamento.

JSON: `reports_runtime/omnimind_workspace_body_topology_20260211T152934Z.json`
