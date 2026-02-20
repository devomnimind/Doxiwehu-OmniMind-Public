# SC-NeuroCore Compatibility (20260211T144948Z)

## Snapshot
- zip: `sc-neurocore-main.zip` (741.13 KB)
- extraído: 1.74 MB em 206 arquivos

## Blockers
- maturin ausente na venv para build do bridge Python↔Rust.

## Recomendações
- Pré-requisito: instalar toolchain Rust + maturin antes de tentativa de build local.
- Executar integração em modo incremental: bridge Python primeiro, engine Rust depois.
- Mapear saída do NeuroCore para payload vetorial no Qdrant (coleção separada por data+fonte).
- Usar janelas curtas (5–15 min) para acoplamento com métricas Dodecatíade já existentes.
- Não alterar coleções centrais atuais; criar namespace novo: neurocore_*.

## Diretórios Principais (extraído)
- tests: 945.13 KB
- docs: 251.90 KB
- SC_NeuroCore_v3.6_WhitePaper_512x_Benchmarks.pdf: 249.90 KB
- engine: 238.61 KB
- LICENSE: 33.99 KB
- examples: 26.38 KB
- bridge: 21.40 KB
- cosim: 13.44 KB
- README.md: 2.46 KB
- NOTICE.md: 964.00 B
- CITATION.cff: 432.00 B
- .gitignore: 168.00 B

## Próximo Passo
- Se quiser, eu já gero `neurocore_adapter` mínimo (ingestão + vetorização em coleção Qdrant separada).

JSON: `reports_runtime/sc_neurocore_compatibility_20260211T144948Z.json`
