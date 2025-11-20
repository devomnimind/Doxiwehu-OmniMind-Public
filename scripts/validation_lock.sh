#!/bin/bash
# OmniMind Validation Lock Script
# Bloqueia mudanças que infrinjam o estado atual do sistema
# Data de criação: 19 de novembro de 2025
# Estado baseline: 1017 testes passando, 2 skipped, 6 warnings

set -e

echo "🔒 OmniMind Validation Lock - Executando validações obrigatórias..."

# Estado baseline esperado
EXPECTED_TESTS_PASSED=1017
EXPECTED_TESTS_SKIPPED=2
EXPECTED_WARNINGS=6

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# 1. Verificar se estamos no repositório correto
if [[ ! -f "requirements.txt" ]] || [[ ! -d "src" ]] || [[ ! -d "tests" ]]; then
    error "Este script deve ser executado na raiz do repositório OmniMind"
    exit 1
fi

log "Verificando estrutura do repositório..."

# 2. Executar formatação de código (black)
log "Executando formatação de código (black)..."
if ! black --check --diff src tests > /dev/null 2>&1; then
    error "Código não está formatado corretamente. Execute: black src tests"
    exit 1
fi
log "✅ Formatação OK"

# 3. Executar linting (flake8) - apenas erros críticos
log "Executando linting (flake8) - verificando apenas erros críticos..."
# Permitir alguns warnings por enquanto, focar em erros críticos
FLAKE8_OUTPUT=$(flake8 src tests --max-line-length=100 --select=E9,F63,F7,F82 2>&1)
if [[ -n "$FLAKE8_OUTPUT" ]]; then
    error "Erros críticos de linting detectados:"
    echo "$FLAKE8_OUTPUT"
    exit 1
fi
log "✅ Linting crítico OK (warnings permitidos temporariamente)"

# 4. Executar type checking (mypy) - modo lenient temporário
log "Executando type checking (mypy) - modo lenient..."
# Temporariamente permitir alguns erros de tipo, focar em erros críticos
MYPY_OUTPUT=$(mypy src tests --show-error-codes 2>&1 | grep -E "(error|note)" | head -20)
if echo "$MYPY_OUTPUT" | grep -q "error"; then
    warning "Erros de tipo detectados (modo lenient ativo):"
    echo "$MYPY_OUTPUT" | head -10
    warning "Erros de tipo permitidos temporariamente - melhore gradualmente"
else
    log "✅ Type checking OK"
fi

# 5. Executar testes e verificar contagens
log "Executando testes completos..."
TEST_OUTPUT=$(python -m pytest tests/ -x --tb=short -q 2>&1)
TEST_EXIT_CODE=$?

if [[ $TEST_EXIT_CODE -ne 0 ]]; then
    error "Testes falharam. Saída completa:"
    echo "$TEST_OUTPUT"
    exit 1
fi

# Parse dos resultados dos testes
PASSED=$(echo "$TEST_OUTPUT" | grep -oP '\d+(?= passed)' | tail -1)
SKIPPED=$(echo "$TEST_OUTPUT" | grep -oP '\d+(?= skipped)' | tail -1)
WARNINGS=$(echo "$TEST_OUTPUT" | grep -oP '\d+(?= warnings)' | tail -1)

# Valores padrão se não encontrados
PASSED=${PASSED:-0}
SKIPPED=${SKIPPED:-0}
WARNINGS=${WARNINGS:-0}

log "Resultados dos testes: $PASSED passed, $SKIPPED skipped, $WARNINGS warnings"

# Verificar se os números batem com o baseline
if [[ $PASSED -lt $EXPECTED_TESTS_PASSED ]]; then
    error "Regressão detectada: $PASSED testes passaram (esperado: $EXPECTED_TESTS_PASSED)"
    error "Mudanças que reduziram a cobertura de testes não são permitidas"
    exit 1
fi

if [[ $SKIPPED -gt $EXPECTED_TESTS_SKIPPED ]]; then
    warning "Aumento no número de testes skipped: $SKIPPED (era: $EXPECTED_TESTS_SKIPPED)"
    warning "Verifique se novos testes foram marcados como skip intencionalmente"
fi

if [[ $WARNINGS -gt $EXPECTED_WARNINGS ]]; then
    warning "Aumento no número de warnings: $WARNINGS (era: $EXPECTED_WARNINGS)"
    warning "Novos warnings foram introduzidos - considere corrigi-los"
fi

# 6. Verificar dependências (pip check)
log "Verificando dependências..."
if ! pip check > /dev/null 2>&1; then
    error "Conflitos de dependências detectados. Execute: pip check"
    exit 1
fi
log "✅ Dependências OK"

# 7. Verificar arquivos core não modificados indevidamente
log "Verificando integridade dos arquivos core..."

CORE_FILES=(
    "src/omnimind_core.py"
    "src/agents/orchestrator_agent.py"
    "src/agents/code_agent.py"
    "src/agents/architect_agent.py"
    "src/agents/debug_agent.py"
    "src/agents/reviewer_agent.py"
    "src/audit/immutable_audit.py"
    "src/security/security_agent.py"
    "requirements.txt"
    "pyproject.toml"
)

for file in "${CORE_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        # Verificar se o arquivo tem conteúdo básico
        if [[ ! -s "$file" ]]; then
            error "Arquivo core vazio ou corrompido: $file"
            exit 1
        fi
    else
        warning "Arquivo core não encontrado: $file"
    fi
done

log "✅ Arquivos core OK"

# 8. Verificar se o ambiente Python está correto
log "Verificando ambiente Python..."
PYTHON_VERSION=$(python --version 2>&1 | grep -oP '\d+\.\d+\.\d+')
if [[ "$PYTHON_VERSION" != "3.12.8" ]]; then
    warning "Python version: $PYTHON_VERSION (esperado: 3.12.8)"
    warning "Certifique-se de estar usando a versão correta do Python"
fi

# Verificar PyTorch
if python -c "import torch; print('PyTorch OK')" > /dev/null 2>&1; then
    log "✅ PyTorch OK"
else
    error "PyTorch não está funcionando corretamente"
    exit 1
fi

log "🎉 Todas as validações passaram!"
log "Estado do sistema: $PASSED testes passando, $SKIPPED skipped, $WARNINGS warnings"
log "✅ Mudanças aprovadas para commit/push"

exit 0