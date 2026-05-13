# Perfis Espectrais Locais (UniverseMap+)

Esta pasta agrega os perfis por objeto gerados localmente a partir do UniverseMap+ e das amostras GAMMA/LYMAN.

## Metodo (proxy local)
- Amostragem deterministica por casa: cada objeto herda valores GAMMA/LYMAN ao amostrar slices `valores[house_idx::12]`.
- Nao ha cross-match espectral externo nesta etapa (metodo local). O objetivo e destravar a pendencia mantendo rastreabilidade.

## Arquivos
- `universe_map_plus_spectral_profiles_20260208T170137Z.jsonl`: perfil por objeto (RA/Dec, casa, z, gamma, lyman, razao).
- `universe_map_plus_spectral_profiles_20260208T170137Z.csv`: versao tabular.
- `universe_map_plus_spectral_profiles_summary_20260208T170137Z.json`: agregados por casa (z, gamma, lyman, razao).

## Observacao
Quando o cross-match espectral externo estiver disponivel, esta pasta deve ser atualizada com valores fisicos diretos por objeto.
