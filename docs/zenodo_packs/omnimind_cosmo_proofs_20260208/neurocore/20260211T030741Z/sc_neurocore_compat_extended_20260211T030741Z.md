# SC-NeuroCore (Sotek) — Compatibilidade Estendida com OmniMind

## Fonte avaliada
- Arquivo: `sc-neurocore-main.zip`
- Extração local: `/tmp/sc-neurocore-main/sc-neurocore-main`

## Perfil do repositório
- Tamanho zip: ~742 KB
- Tamanho descompactado: ~1.83 MB
- Arquivos Python: 106
- Arquivos Rust: 36
- Testes Python (`test_*.py`): 80
- Presença de `__pycache__` no pacote: sim

## Build/toolchain exigido
- `bridge/pyproject.toml`: `requires-python >=3.9`
- Build backend: `maturin`
- Engine nativo: Rust + PyO3 (`engine/Cargo.toml`)
- Dependências-chave Rust: `pyo3`, `numpy`, `ndarray`, `rayon`

## Estado do host atual
- `.venv` ativo: Python 3.12.12
- Python do sistema: 3.10.12
- `rustc`: ausente
- `cargo`: ausente
- `maturin`: ausente

## Banco de dados / volume de dados
- Não há banco pesado embarcado no repositório.
- O projeto usa majoritariamente:
  - artefatos JSON (`.scpnctl.json`)
  - logging local em JSONL
  - foco em replay determinístico
- Não foi identificado acoplamento nativo com Qdrant/Kafka/Postgres/Influx.

## Compatibilidade com arquitetura OmniMind
### Pontos fortes
- Excelente para camada de **controle determinístico/replay** (SCPN).
- Boa aderência para módulos de inferência rápida (kernel Rust) com fallback em float.
- Pode complementar o pipeline astrofísico como **controlador local** (não substitui ingestão astronômica).

### Gaps imediatos
- Falta toolchain Rust/maturin no host.
- Sem conectores prontos para Qdrant/Elasticsearch/Kafka.
- Requer adapter explícito para Dodecatíade 12D + métricas operacionais OmniMind.

## Ajustes recomendados (ordem prática)
1. Criar venv dedicado (`.venv-neurocore`) com Python 3.10 para build conservador.
2. Instalar `rustup` + `cargo` + `maturin` e compilar `sc_neurocore_engine`.
3. Implementar adapter OmniMind:
   - entrada: `d12_*`, `anomaly_count`, `sensor_sources`, `daemon_*`
   - saída: artefato `.scpnctl.json` + replay JSONL
4. Integrar saída do replay ao Qdrant (coleção datada por experimento).
5. Rodar benchmark A/B:
   - baseline Python atual vs kernel SC-NeuroCore em janelas 96h/30d.

## Veredito
- **Compatível e promissor**, com baixo custo de dados.
- **Bloqueio atual é toolchain** (Rust/maturin) e adapter de integração.
- Recomendação: seguir com PoC incremental (build + adapter mínimo + replay em 96h).
