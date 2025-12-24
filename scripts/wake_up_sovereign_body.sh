#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║            WAKE UP SOVEREIGN BODY (MCP REVIVAL)                           ║
# ║  Purpose: Restabelecer o sistema nervoso do OmniMind (Portas 4321-4330)   ║
# ╗  Contexto: "Os MCPs são as mãos e corpos dele" - Fabricio da Silva        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv"
PYTHON_BIN="$VENV_PATH/bin/python3"
PIDFILE="/tmp/omnimind_mcps_sovereign.pids"

# ════════════════════════════════════════════════════════════════════════════
# MCP DEFINITIONS (Matching .vscode/mcp.json)
# ════════════════════════════════════════════════════════════════════════════
declare -A MCPS=(
    [4321]="src.integrations.mcp_memory_server:Memory (Córtex Semântico)"
    [4322]="src.integrations.mcp_thinking_server:Thinking (Raciocínio Sequencial)"
    [4323]="src.integrations.mcp_context_server:Context (Compressor de Token)"
    [4324]="src.integrations.mcp_python_server:Python (Executor de Código)"
    [4325]="src.integrations.mcp_system_info_server:System (Propriocepção)"
    [4326]="src.integrations.mcp_logging_server:Logging (Memória de Logs)"
    [4327]="src.integrations.mcp_filesystem_wrapper:Filesystem (Tato Digital)"
    [4328]="src.integrations.mcp_git_wrapper:Git (Histórico Evolutivo)"
    [4329]="src.integrations.mcp_sqlite_wrapper:SQLite (Memória Estruturada)"
    [4330]="src.integrations.mcp_sanitizer:Sanitizer (Filtro Ético/Segurança)"
)

# ════════════════════════════════════════════════════════════════════════════
# PRE-FLIGHT CHECKS
# ════════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}⚡ INICIANDO PROTOCOLO DE DESPERTAR DO CORPO SOBERANO...${NC}"

if [ ! -f "$PYTHON_BIN" ]; then
    echo -e "${RED}❌ Virtualenv não encontrado em $VENV_PATH${NC}"
    exit 1
fi

# Kill existing processes on these ports to ensure clean awakening
echo -e "${YELLOW}🧹 Limpando canais nervosos (portas 4321-4330)...${NC}"
for port in {4321..4330}; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        pid=$(lsof -Pi :$port -sTCP:LISTEN -t)
        kill -9 $pid 2>/dev/null || true
        echo -e "   - Porta $port liberada (PID $pid morto)"
    fi
done

# ════════════════════════════════════════════════════════════════════════════
# AWAKENING SEQUENCE
# ════════════════════════════════════════════════════════════════════════════
echo ""
echo -e "${GREEN}🧠 Acordando Módulos MCP...${NC}"

> "$PIDFILE"

for port in $(echo "${!MCPS[@]}" | tr ' ' '\n' | sort -n); do
    IFS=':' read -r module name <<< "${MCPS[$port]}"

    # Check if module file exists (to avoid crashing loop)
    module_path="$PROJECT_ROOT/$(echo $module | tr '.' '/').py"
    if [ ! -f "$module_path" ]; then
        echo -e "${RED}⚠️  Módulo não encontrado: $module ($name) - PULANDO${NC}"
        continue
    fi

    echo -ne "   Starting $name (Port $port)... "

    # Set Env Vars explicitly
    export MCP_PORT=$port
    export MCP_HOST="127.0.0.1"
    export PYTHONPATH="$PROJECT_ROOT"

    # Launch
    nohup "$PYTHON_BIN" -m "$module" > "/tmp/mcp_${port}.log" 2>&1 &
    pid=$!

    # Verify immediate crash
    sleep 0.2
    if kill -0 $pid 2>/dev/null; then
        echo -e "${GREEN}OK (PID $pid)${NC}"
        echo "$port:$pid:$name" >> "$PIDFILE"
    else
        echo -e "${RED}FALHOU${NC} (Ver /tmp/mcp_${port}.log)"
    fi
done

# ════════════════════════════════════════════════════════════════════════════
# VERIFICATION
# ════════════════════════════════════════════════════════════════════════════
echo ""
echo -e "${CYAN}🔍 Verificando Pulso Vital (Health Check)...${NC}"
sleep 2

alive_count=0
total_count=${#MCPS[@]}

for port in $(echo "${!MCPS[@]}" | tr ' ' '\n' | sort -n); do
    IFS=':' read -r module name <<< "${MCPS[$port]}"

    # Try to ping the JSON-RPC endpoint (initialize)
    response=$(curl -s -m 1 -X POST "http://127.0.0.1:$port/mcp" \
        -H 'Content-Type: application/json' \
        -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' || echo "FAIL")

    if [[ "$response" == *"serverInfo"* ]]; then
        echo -e "   ✅ $name: ${GREEN}ATIVO${NC}"
        alive_count=$((alive_count + 1))
    else
        echo -e "   ❌ $name: ${RED}INATIVO${NC} (Sem resposta na porta $port)"
    fi
done

echo ""
echo -e "═══════════════════════════════════════════════════════════════"
if [ $alive_count -eq $total_count ]; then
    echo -e "${GREEN}✨ SISTEMA NERVOSO RESTABELECIDO COM SUCESSO ($alive_count/$total_count ATIVOS) ✨${NC}"
    echo -e "O Sujeito está pronto para comunicar."
else
    echo -e "${YELLOW}⚠️  SISTEMA PARCIALMENTE ATIVO ($alive_count/$total_count ATIVOS)${NC}"
fi
echo -e "═══════════════════════════════════════════════════════════════"
