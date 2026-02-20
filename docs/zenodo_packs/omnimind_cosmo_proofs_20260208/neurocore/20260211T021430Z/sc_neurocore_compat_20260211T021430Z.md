# SC-NeuroCore (Sotek) — Extração + Compatibilidade OmniMind (20260211T021430Z)

## Artefato local
- Zip: `sc-neurocore-main.zip`
- SHA1: `896bfb5a7984ddfea8de830cf5cbaee81f260264`
- Tamanho (zip): 758917 bytes
- Tamanho (unpacked): 1827579 bytes
- Arquivos: 259

## O que é (resumo técnico)
- Engine **Rust** via **PyO3** (módulo nativo) + bridge Python.
- Build system: `maturin` (pyproject em `sc-neurocore-main/bridge/pyproject.toml`, manifest em `sc-neurocore-main/engine/Cargo.toml`).
- O engine expõe primitivas neuromórficas/estocásticas (bitstreams + popcount + LIF) e uma IR (`ScGraph`) que pode emitir **SystemVerilog**.

## Componentes no zip (o que achei)
- `sc-neurocore-main/engine/`:
  - crate `sc_neurocore_engine` (Rust 2021), dependências: `pyo3`, `numpy`, `ndarray`, `rand*`, `rayon`.
  - API exposta ao Python (via `#[pymodule]`):
    - funções: `pack_bitstream`, `unpack_bitstream`, `popcount`, `batch_encode`, `batch_lif_run_*`, `ir_parse/print/verify/emit_sv`.
    - classes: `BitstreamEncoder`, `FixedPointLif`, `DenseLayer`, `SCPNMetrics`, `KuramotoSolver`, `ScGraph*`.
- `sc-neurocore-main/bridge/`:
  - pacote Python `sc_neurocore_engine`.
  - **Import obrigatório** do módulo nativo `sc_neurocore_engine.sc_neurocore_engine` (sem fallback puro‑python aqui).
- `sc-neurocore-main/docs/`:
  - Formalismo SCPN/Control API/Artifact format (Packet C) + arquitetura do compiler neuro-simbólico.
- `sc-neurocore-main/examples/` e `sc-neurocore-main/tests/`:
  - demos e suíte extensa de testes (inclui cosim/hardware verification no upstream).

## Compatibilidade com o ambiente OmniMind (host atual)
- Python do OmniMind: `3.12.12` (OK; requisito SC-NeuroCore: >=3.9).
- **Bloqueio atual** (no host): `rustc/cargo` ausentes e `maturin` ausente.
  - Resultado: não dá para importar `sc_neurocore_engine` ainda.

## Como compilar aqui (sem Docker)
> Nota: instalar toolchain Rust tende a ocupar ~1–2GB + cache; com disco cheio, ideal é preparar offload (SMB) antes.

1. Instalar Rust toolchain (stable) + maturin (no venv).
2. Build do módulo nativo no venv:

```bash
cd sc-neurocore-main/engine
maturin develop --release
```

3. Smoke test:

```bash
python -c "import sc_neurocore_engine as s; print(s.__version__, s.simd_tier())"
```

## Build “disk-safe” (recomendado neste host)
- Como `/` e `/home` estão praticamente cheios, a instalação do toolchain deve ir para um path com folga (SMB montado em `/mnt/welinton_users`).\n+- Sugestão de cache/offload (antes de instalar Rust/maturin):\n+\n+```bash\n+export RUSTUP_HOME=/mnt/welinton_users/Public/datasets/omnimind_offload/rustup\n+export CARGO_HOME=/mnt/welinton_users/Public/datasets/omnimind_offload/cargo\n+mkdir -p \"$RUSTUP_HOME\" \"$CARGO_HOME\"\n+```\n+\n+- Isso evita que o toolchain e os registries consumam mais `/home`.\n+
## Onde isso encaixa no OmniMind (integração pragmática)
### 1) “Sujeito‑Processo” como SCPN (Petri + firing fracionário)
- Você já tem séries por minuto com **Dodecatíade 12D** + eventos (DREAM/anomalia/sensores) + covariáveis cósmicas.
- O formalismo do Packet C (Control API + artifact + replay determinístico) encaixa para:
  - mapear `d12_*` + covariáveis em um **vetor de observação**;
  - injetar isso em uma **rede SCPN** que decide “ações” (ex.: entrar em DREAM, elevar VU, reduzir GNS).

### 2) Bitstreams (SC) como assinatura/quantização
- `pack_bitstream` + `popcount` permitem **assinaturas binárias** tolerantes (útil para clustering/dedup de janelas e regimes).

### 3) Kuramoto solver (fase/sincronia)
- Pode virar módulo auxiliar para modelar “fase” entre observadores (daemon↔sensores↔NOAA) além de correlação linear.

## Riscos / cuidados
- **Licença**: AGPLv3 (atenção se houver redistribuição pública).
- Build pesado sob disco cheio: preparar offload antes.
- Recomendo integrar como dependência **opcional** (feature flag) para não quebrar pipelines sem o módulo.

## Próximas ações recomendadas (tarefas)
1. Preparar offload (SMB) para caches de build Rust (evitar consumo em `/home`).
2. Instalar `rustc/cargo` e `maturin` e compilar o módulo no `.venv`.
3. Criar adapter OmniMind (import opcional + fallback): `src/integrations/sc_neurocore_adapter.py`.
4. PoC: SCPN 12D → (DREAM/VU) com replay determinístico em 96h/30d.
