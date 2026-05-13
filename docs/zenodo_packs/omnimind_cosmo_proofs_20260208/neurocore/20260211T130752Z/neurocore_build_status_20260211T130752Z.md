# NeuroCore Build Status (20260211T130752Z)

## Rust
- rustc: `rustc 1.93.0 (254b59607 2026-01-19)`
- cargo: `cargo 1.93.0 (083ac5135 2025-12-15)`

## Venvs
- `.venv`: Python 3.12.12 | pkgs={'qdrant-client': '1.16.2', 'numpy': '2.3.5', 'pandas': '2.3.3'}
- `.venv312`: Python 3.12.12 | pkgs={'numpy': '2.4.1'}
- `.venv_proxy`: Python 3.12.12 | pkgs={'numpy': '2.4.2'}
- `.venv_satellite`: Python 3.12.12 | pkgs={'qdrant-client': '1.16.2', 'numpy': '2.3.5'}
- `.venv_neurocore`: Python 3.10.12 | pkgs={'maturin': '1.11.5', 'numpy': '2.2.6', 'sc-neurocore-engine': '3.6.0'}

## NeuroCore Build
- maturin develop --release: `True`
- artifact: `sc-neurocore-main/bridge/sc_neurocore_engine/sc_neurocore_engine.cpython-310-x86_64-linux-gnu.so`
- collections (adapter):
  - `neurocore_adapter_20260211_124411`
  - `neurocore_adapter_20260211_4000`
  - `neurocore_adapter_20260211_10000`
  - `neurocore_adapter_20260211_10kstack`
