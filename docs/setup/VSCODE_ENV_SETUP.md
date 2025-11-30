# OmniMind Development Startup Guide

## 🚨 Solução para Erro: "python.terminal.useEnvFile"

O VS Code estava bloqueando porque o terminal não estava injetando as variáveis de ambiente do `.env`.

### ✅ Solução Implementada

1. **Settings.json** (`.vscode/settings.json`):
   - `"python.terminal.useEnvFile": true` ✅
   - `"python.envFile": "${workspaceFolder}/.env"`
   - `"python.terminal.activateEnvironment": true`

2. **Tasks adicionadas** (`.vscode/tasks.json`):
   - `omnimind-cleanup`: Mata processos antigos
   - `🚀 Start Development`: Inicia Backend + Frontend limpo
   - `🧪 Test Backend Endpoint`: Testa /audit/stats
   - `🏥 Health Check`: Verifica status

3. **Launch Configurations** (`.vscode/launch.json`):
   - `🚀 OmniMind Dev (Backend + Frontend)`: Compound launch
   - `🔧 Backend (Simple)`: Python + PYTHONPATH injetado
   - `🎨 Frontend (Vite)`: Node/npm dev server

4. **Script de Startup** (`./start_development.sh`):
   - Limpa processos antigos
   - Ativa `.venv`
   - Seta `PYTHONPATH`
   - Inicia Backend (porta 9000)
   - Inicia Frontend (porta 3000)

## 🚀 Como Usar

### Opção 1: VS Code Debugger (Recomendado)
1. Abrir Command Palette: `Ctrl+Shift+D`
2. Selecionar: **"🚀 OmniMind Dev (Backend + Frontend)"**
3. Pressionar F5 ou clique em "Start Debugging"

### Opção 2: Tasks
1. Abrir Command Palette: `Ctrl+Shift+B`
2. Selecionar: **"🚀 Start Development (Backend + Frontend)"**

### Opção 3: Terminal Manual
```bash
cd /home/fahbrain/projects/omnimind
source .venv/bin/activate
export PYTHONPATH="./src:."
bash ./start_development.sh
```

## 📊 Verificar Status

**Health Check da API:**
```bash
curl -i http://127.0.0.1:9000/health
# Esperado: HTTP/1.1 200 OK {"status":"ok"}
```

**Dados de Auditoria (Reais, não hardcoded):**
```bash
curl -u admin:omnimind2025! http://127.0.0.1:9000/audit/stats | json_pp
# Esperado: {"total_events": 303, "chain_integrity": true, ...}
```

**Dashboard:**
- Abrir: `http://localhost:3000`
- User: `admin`
- Pass: `omnimind2025!`
- Verificar QuickStatsCards mostra **303** eventos (real, não 1797)

## 🔧 Configurações Críticas

### `.vscode/settings.json`
```jsonc
"python.terminal.useEnvFile": true,  // 🚨 CRÍTICO: Força injeção .env
"python.envFile": "${workspaceFolder}/.env",
"python.terminal.activateEnvironment": true,
"python.terminal.activateEnvInCurrentTerminal": true,
```

### `.env` (Root do projeto)
```dotenv
PYTHONPATH=./src:.
PYTHONUNBUFFERED=1
OMNIMIND_DASHBOARD_USER=admin
OMNIMIND_DASHBOARD_PASS=omnimind2025!
VITE_API_URL=http://localhost:9000
VITE_DASHBOARD_USER=admin
VITE_DASHBOARD_PASS=omnimind2025!
```

### `web/frontend/.env`
```dotenv
VITE_API_URL=http://localhost:9000
VITE_DASHBOARD_USER=admin
VITE_DASHBOARD_PASS=omnimind2025!
```

## 🧹 Limpeza Manual

Se as coisas ficarem estranhas:

```bash
# Matar tudo
pkill -9 -f "simple_backend|uvicorn|vite|npm"

# Verificar portas em uso
lsof -i :9000
lsof -i :3000

# Iniciar limpo
cd /home/fahbrain/projects/omnimind
source .venv/bin/activate
python simple_backend.py
# Em outro terminal:
cd web/frontend
npm run dev
```

## 📝 Log de Mudanças

- ✅ Created `.vscode/tasks.json` - omnimind-cleanup, Start Development tasks
- ✅ Updated `.vscode/launch.json` - Compound launch for Backend+Frontend
- ✅ Updated `.vscode/settings.json` - Forced python.terminal.useEnvFile=true
- ✅ Created `start_development.sh` - Clean startup script
- ✅ Updated `web/frontend/.env` - VITE_API_URL=http://localhost:9000

## 🆘 Troubleshooting

**Problema:** Terminal mostra "environment file is configured but terminal environment injection is disabled"
- **Solução:** ✅ Já configurado em settings.json, feche e reabra VS Code

**Problema:** Backend não inicia na porta 9000
```bash
lsof -i :9000  # Ver o que está usando
pkill -9 -f simple_backend  # Matar processo
```

**Problema:** Frontend não compila
```bash
cd web/frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Problema:** Import errors em Python
```bash
# Verificar PYTHONPATH
echo $PYTHONPATH
# Deve ser: ./src:.

# Ou manualmente
export PYTHONPATH="$(pwd)/src:."
```

---

**Status:** ✅ OmniMind Development Environment Ready for Use
**Last Updated:** 2025-11-29 11:58
