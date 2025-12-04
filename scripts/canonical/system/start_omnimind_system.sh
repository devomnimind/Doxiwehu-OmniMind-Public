#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Iniciando Sistema OmniMind Completo...${NC}"

# 🔧 CRÍTICO: Ativar venv ANTES de qualquer import Python
# PROJECT_ROOT deve apontar para a raiz do projeto (3 níveis acima de scripts/canonical/system)
PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
    echo "✅ Venv ativado: $VIRTUAL_ENV"
else
    echo "⚠️  Venv não encontrado em $PROJECT_ROOT/.venv"
fi

# Garantir permissão de execução no run_cluster
chmod +x scripts/canonical/system/run_cluster.sh

# 1. Limpeza
echo "🧹 Limpando processos antigos..."
pkill -f "python web/backend/main.py"
pkill -f "uvicorn web.backend.main:app"
pkill -f "vite"
pkill -f "bpftrace.*monitor_mcp_bpf" || true
sleep 2

# 2. Iniciar Backend Cluster
echo -e "${GREEN}🔌 Iniciando Backend Cluster...${NC}"
./scripts/canonical/system/run_cluster.sh

# Aguardar Backend subir
# ⚠️ CRÍTICO: Uvicorn + Orchestrator + SecurityAgent podem levar 30-60s
# Aumentado de 10s para 40s para garantir inicialização completa
echo "⏳ Aguardando Backend inicializar (40s - Orchestrator + SecurityAgent)..."
sleep 40

# Verificar Health Check (usando o endpoint /health/ que agora é servido pelo router)
# Nota: O endpoint raiz /health foi removido do main.py, agora é /health/ (com barra) ou /health (se o router permitir sem barra)
# O router tem prefix="/health" e @router.get("/"). Então é /health/
if curl -s http://localhost:8000/health/ > /dev/null; then
    echo -e "${GREEN}✅ Backend (Primary) Online!${NC}"
elif curl -s http://localhost:8000/api/v1/status > /dev/null; then
    echo -e "${GREEN}✅ Backend (Primary) Online (via Status API)!${NC}"
else
    echo -e "${RED}❌ Falha ao conectar no Backend (Port 8000). Verifique logs/backend_8000.log${NC}"
    tail -n 10 logs/backend_8000.log
fi

# 3. Iniciar Daemon (com delay para não sobrecarregar)
echo -e "${GREEN}⏰ Agendando inicialização do Daemon (em 5 segundos)...${NC}"
sleep 5
echo -e "${GREEN}🤖 Inicializando OmniMind Daemon...${NC}"
cd "$PROJECT_ROOT"

# Usar credenciais padrão do dashboard (admin:omnimind2025!)
# Fazer requisição com autenticação básica
curl -X POST http://localhost:8000/daemon/start \
  -u admin:omnimind2025! \
  > logs/daemon_start.log 2>&1 &
DAEMON_START_PID=$!
echo "✓ Daemon start request enviado (PID $DAEMON_START_PID)"
sleep 2

# 4. Iniciar Frontend
echo -e "${GREEN}🎨 Iniciando Frontend...${NC}"
cd web/frontend
# Verificar se node_modules existe, se não, instalar
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências do Frontend..."
    npm install
fi

nohup npm run dev > ../../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../../logs/frontend.pid
echo "Frontend iniciado com PID $FRONTEND_PID"

# 5. Verificação Final
echo -e "${GREEN}🔍 Verificando status do sistema...${NC}"
sleep 5

if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Frontend rodando (PID $FRONTEND_PID)${NC}"
    echo "   Acesse: http://localhost:3000"
else
    echo -e "${RED}❌ Frontend falhou ao iniciar. Verifique logs/frontend.log${NC}"
    cat ../../logs/frontend.log
fi

# 6. Iniciar eBPF Monitor Contínuo
echo -e "${GREEN}📊 Iniciando eBPF Monitor Contínuo...${NC}"

# Voltar para a raiz do projeto para encontrar scripts/secure_run.py
cd "$PROJECT_ROOT"

if command -v bpftrace &> /dev/null; then
    EBPF_LOG="logs/ebpf_monitor.log"
    mkdir -p logs

    # Garantir permissões no arquivo de log se ele existir
    if [ -f "$EBPF_LOG" ]; then
        # Tentar mudar dono para usuário atual se possível, ou remover se falhar
        if ! touch "$EBPF_LOG" 2>/dev/null; then
            echo "⚠️  Sem permissão de escrita em $EBPF_LOG. Tentando remover com sudo..."
            sudo rm -f "$EBPF_LOG"
        fi
    fi

    # Parar eBPF anterior
    python3 scripts/secure_run.py pkill -f "bpftrace.*monitor_mcp_bpf" || true
    sleep 1
    # Iniciar em background
    # Nota: secure_run.py já lida com sudo -n
    python3 scripts/secure_run.py bpftrace scripts/monitor_mcp_bpf.bt > "${EBPF_LOG}" 2>&1 &
    sleep 2
    echo -e "${GREEN}✅ eBPF Monitor ativo${NC}"
    echo "   Log: tail -f ${EBPF_LOG}"
else
    echo -e "${RED}⚠️  bpftrace não encontrado. Instale com: sudo apt install bpftrace${NC}"
fi

echo -e "${GREEN}✨ Sistema OmniMind Reiniciado!${NC}"
echo "Backend Cluster: Ports 8000, 8080, 3001"
echo "Frontend: http://localhost:3000"
echo "eBPF Monitor: logs/ebpf_monitor.log"
echo "Logs Directory: logs/"
