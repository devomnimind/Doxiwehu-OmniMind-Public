# OmniMind Dashboard Frontend

Lightweight React/Vite UI that consumes the FastAPI dashboard service and visualizes plan progress, MCP/D-Bus flows, metrics, and authenticated controls.

## Requisitos

- Node.js (>=20)
- npm (>=9)
 - Serve o backend FastAPI em `http://localhost:8000` (ou ajuste `VITE_API_BASE`)

## Instalação

```bash
cd /home/fahbrain/projects/omnimind/web/frontend
npm install
```

## Execução

```bash
npm run dev -- --host 0.0.0.0 --port 4173
```

Use `http://localhost:4173` in the browser while the FastAPI backend runs on `http://localhost:8000` and configure login credentials via `OMNIMIND_DASHBOARD_USER`/`OMNIMIND_DASHBOARD_PASS`.
