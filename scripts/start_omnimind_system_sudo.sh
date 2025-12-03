#!/bin/bash

# ============================================================================
# 🔐 OMNIMIND SYSTEM START WITH SUDO ELEVATION
# ============================================================================
# Este script é um wrapper que:
# 1. Detecta se precisa sudo
# 2. Executa com sudo se necessário
# 3. Passa todas as variáveis de ambiente necessárias
# 4. Não pede senha (usa sudoers preauth)
# ============================================================================

set -e

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Função para rodar comando com sudo se necessário
run_sudo_if_needed() {
    local cmd="$1"

    # Verifica se precisa sudo (para operações eBPF)
    if echo "$cmd" | grep -q "bpftrace\|eBPF\|monitor_mcp_bpf"; then
        # Tenta com sudo, mas com variables de ambiente
        sudo -E bash -c "$cmd"
    else
        # Comandos normais rodam sem sudo
        bash -c "$cmd"
    fi
}

echo -e "${GREEN}🚀 Iniciando Sistema OmniMind (Com Elevação)...${NC}"

# 1. Garantir permissões no script principal
chmod +x "$SCRIPT_DIR/start_omnimind_system.sh"
chmod +x "$SCRIPT_DIR/canonical/system/run_cluster.sh" 2>/dev/null || true

# 2. Tentar executar o script principal
# Se falhar por permissão, tenta com sudo
if ! bash "$SCRIPT_DIR/start_omnimind_system.sh"; then
    echo -e "${YELLOW}⚠️  Script falhou sem sudo, tentando com elevação...${NC}"

    # Passa variáveis de ambiente importantes via -E
    sudo -E bash "$SCRIPT_DIR/start_omnimind_system.sh"
else
    echo -e "${GREEN}✅ Script completado com sucesso${NC}"
fi
