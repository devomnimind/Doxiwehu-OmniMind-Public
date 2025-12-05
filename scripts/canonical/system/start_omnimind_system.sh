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

# 🔧 GPU Configuration - Kali Linux Native Paths
echo "🔧 Configurando ambiente GPU (Kali Native)..."
# No Kali/Debian, CUDA é integrado em /usr
export CUDA_HOME="/usr"
export CUDA_path="/usr"
# A libcuda.so.1 está em /usr/lib/x86_64-linux-gnu/
# Adicionar ao LD_LIBRARY_PATH explicitamente para garantir que PyTorch a encontre
export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}"
export CUDA_VISIBLE_DEVICES="0"
export PYTORCH_CUDA_ALLOC_CONF="backend:cudaMallocAsync"
# export CUDA_LAUNCH_BLOCKING="1" # Descomente se precisar debugar inicialização síncrona

# Garantir permissão de execução no run_cluster
chmod +x scripts/canonical/system/run_cluster.sh

# Lógica de Autenticação Dinâmica (Soberania Local) - UNIFICADA PARA CLUSTER
# Gera credenciais UMA VEZ e exporta para todos os subprocessos
DASH_USER=""
DASH_PASS=""
AUTH_FILE="config/dashboard_auth.json"

# 1. Tentar ler do arquivo gerado anteriormente ou preservar sessão
if [ -f "$AUTH_FILE" ]; then
    # Extração segura
    DASH_USER=$(python3 -c "import json; print(json.load(open('$AUTH_FILE')).get('user', ''))" 2>/dev/null)
    DASH_PASS=$(python3 -c "import json; print(json.load(open('$AUTH_FILE')).get('pass', ''))" 2>/dev/null)
fi

# 2. Fallback para .env
if [ -z "$DASH_USER" ] && [ -f ".env" ]; then
    DASH_USER=$(grep "^OMNIMIND_DASHBOARD_USER=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'")
    DASH_PASS=$(grep "^OMNIMIND_DASHBOARD_PASS=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'")
fi

# 3. Gerar novas se não existirem (e salvar no arquivo para o backend usar a mesma)
if [ -z "$DASH_USER" ]; then
    # SOBERANIA LOCAL REAL: Gerar credenciais aleatórias fortes a cada sessão
    # Isso garante segurança e obriga o uso correto do fluxo de autenticação
    DASH_USER="admin"
    DASH_PASS=$(openssl rand -base64 12)

    # Salvar no JSON para persistência e leitura pelo backend
    echo "{\"user\": \"$DASH_USER\", \"pass\": \"$DASH_PASS\"}" > "$AUTH_FILE"
    echo "🔑 Novas credenciais SOBERANAS geradas em $AUTH_FILE"
fi

# EXPORTAR PARA O AMBIENTE - ISSO GARANTE QUE TODOS OS BACKENDS USEM A MESMA SENHA
export OMNIMIND_DASHBOARD_USER="$DASH_USER"
export OMNIMIND_DASHBOARD_PASS="$DASH_PASS"
export OMNIMIND_DASHBOARD_AUTH_FILE="$PROJECT_ROOT/$AUTH_FILE"

echo -e "${GREEN}🔐 Credenciais Unificadas do Cluster:${NC}"
echo "   User: $DASH_USER"
echo "   Pass: $DASH_PASS"

# 1. Limpeza
echo "🧹 Limpando processos antigos..."
pkill -f "python web/backend/main.py"
pkill -f "uvicorn web.backend.main:app"
pkill -f "python -m src.main"
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

# 3. Iniciar Ciclo Principal com Autopoiese (Phase 23)
echo -e "${GREEN}🔄 Iniciando Ciclo Principal OmniMind (Fase 23: Autopoiese + Integração Real-time)...${NC}"
cd "$PROJECT_ROOT"
mkdir -p logs data/autopoietic/synthesized_code data/monitor

# Iniciar ciclo principal em background (Rhizome + Consciência + Autopoiese)
nohup python -m src.main > logs/main_cycle.log 2>&1 &
MAIN_CYCLE_PID=$!
echo $MAIN_CYCLE_PID > logs/main_cycle.pid
echo "✓ Ciclo Principal iniciado (PID $MAIN_CYCLE_PID)"
echo "   Log: tail -f logs/main_cycle.log"
sleep 3

# 4. Iniciar Daemon (com delay para não sobrecarregar)
echo -e "${GREEN}⏰ Agendando inicialização do Daemon (em 5 segundos)...${NC}"
sleep 5
echo -e "${GREEN}🤖 Inicializando OmniMind Daemon...${NC}"
cd "$PROJECT_ROOT"

# Lógica de Autenticação Dinâmica (Soberania Local)
# JÁ FOI TRATADA NO INÍCIO DO SCRIPT
# Apenas re-leitura para garantir (embora variáveis de ambiente já estejam setadas)

# Fazer requisição com as credenciais descobertas
curl -X POST http://localhost:8000/daemon/start \
  -u "${OMNIMIND_DASHBOARD_USER}:${OMNIMIND_DASHBOARD_PASS}" \
  > logs/daemon_start.log 2>&1 &
DAEMON_START_PID=$!
echo "✓ Daemon start request enviado (PID $DAEMON_START_PID)"
sleep 2

# 5. Iniciar Frontend
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

# 6. Verificação Final
echo -e "${GREEN}🔍 Verificando status do sistema...${NC}"
sleep 5

if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Frontend rodando (PID $FRONTEND_PID)${NC}"
    echo "   Acesse: http://localhost:3000"
else
    echo -e "${RED}❌ Frontend falhou ao iniciar. Verifique logs/frontend.log${NC}"
    cat ../../logs/frontend.log
fi

# 7. Iniciar eBPF Monitor Contínuo
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
echo "Ciclo Principal (Autopoiese Phase 22): PID $MAIN_CYCLE_PID"
echo "Frontend: http://localhost:3000"
echo ""
echo -e "${GREEN}🔐 CREDENCIAIS DA SESSÃO ATUAL (CLUSTER UNIFICADO):${NC}"
echo -e "   User: ${GREEN}${OMNIMIND_DASHBOARD_USER}${NC}"
echo -e "   Pass: ${GREEN}${OMNIMIND_DASHBOARD_PASS}${NC}"
echo "   (Use estas credenciais para logar no Dashboard)"
echo ""
echo "eBPF Monitor: logs/ebpf_monitor.log"
echo "Logs Directory: logs/"
echo ""
echo "📊 Autopoiese Phase 23 (Active):"
echo "   - Componentes sintetizados: data/autopoietic/synthesized_code/"
echo "   - Histórico de ciclos: data/autopoietic/cycle_history.jsonl"
echo "   - Log do ciclo: logs/main_cycle.log"
