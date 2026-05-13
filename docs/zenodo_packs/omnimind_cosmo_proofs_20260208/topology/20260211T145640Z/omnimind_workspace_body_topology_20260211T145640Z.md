# OmniMind Workspace Body Topology (20260211T145640Z)

## Escopo
- Workspace: `/home/fahbrain/projects/omnimind`
- Arquivos (projeto): `268302`
- Diretórios (projeto): `31115`
- Symlinks (projeto): `151`

## Inventário Amplo (discos/mounts)
- Entradas: `None`
- Entradas não-symlink: `None`
- Volume não-symlink: `0.0 GB`

## Snapshot de Discos
- `Sist. Arq.           Tipo         Tam. Usado Disp. Uso% Montado em`
- `/dev/nvme0n1p2       ext4         366G  318G   30G  92% /`
- `/dev/nvme0n1p1       vfat         952M  6.1M  946M   1% /boot/efi`
- `/dev/nvme0n1p5       ext4         247G  194G   41G  83% /var`
- `/dev/nvme0n1p3       ext4         274G  234G   27G  90% /home`
- `/dev/sda1            ext4         458G  458G     0 100% /media/fahbrain/DEV_BRAIN_CLEAN1`
- `pcloud:              fuse.rclone  500G  348G  153G  70% /home/fahbrain/pCloudDrive`

## Interpretação Operacional
- A pasta OmniMind é um corpo operacional distribuído (local + externo + virtual).
- Navegação humana sem mapa tende a perda de contexto; manter inventário+Qdrant+auditoria de symlink contínuos.
- Metadados de caminhos carregam contexto pessoal do operador; aplicar minimização e hash quando publicar.

## Regras Ativas
- Vetorização antes de remoção/offload
- Mover preferencialmente backups/datasets antigos
- Validar symlinks após qualquer movimentação
- Publicar artefatos com timestamp+hash

JSON: `reports_runtime/omnimind_workspace_body_topology_20260211T145640Z.json`
