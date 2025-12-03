#!/bin/bash

# ============================================================================
# 🧠 RUN TESTS WITH OMNIMIND AUTODEFENSE
# ============================================================================
# Executa suite completa com:
# - GPU ativada
# - Dev mode
# - Debug ativo
# - Timeouts adaptativos (220-800s)
# - OmniMind TestDefense ativado (detecta testes perigosos)
# - Logs profundos em arquivos com timestamp
# ============================================================================

set -e

cd /home/fahbrain/projects/omnimind

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="data/test_reports"
mkdir -p "$LOG_DIR"

echo "🧪 OMNIMIND TEST SUITE COM AUTODEFESA"
echo "======================================"
echo "⏱️  Timestamp: $TIMESTAMP"
echo "📊 Testes esperados: ~3952"
echo "🛡️  Modo: Autodefesa ativada"
echo "======================================"
echo ""

# Comando completo com GPU + Dev + Debug
OMNIMIND_GPU=true \
OMNIMIND_DEV=true \
OMNIMIND_DEBUG=true \
pytest tests/ \
  -vv \
  --tb=short \
  --log-cli-level=DEBUG \
  --log-file="$LOG_DIR/pytest_${TIMESTAMP}.log" \
  --junit-xml="$LOG_DIR/junit_${TIMESTAMP}.xml" \
  --html="$LOG_DIR/report_${TIMESTAMP}.html" \
  --self-contained-html \
  --durations=20 \
  -s \
  2>&1 | tee "$LOG_DIR/output_${TIMESTAMP}.log"

EXIT_CODE=$?

echo ""
echo "======================================"
echo "✅ TESTES FINALIZADOS"
echo "======================================"
echo "📋 Logs salvos em: $LOG_DIR"
echo "   - output_${TIMESTAMP}.log (stdout/stderr)"
echo "   - pytest_${TIMESTAMP}.log (pytest logs)"
echo "   - junit_${TIMESTAMP}.xml (CI/CD report)"
echo "   - report_${TIMESTAMP}.html (dashboard)"
echo ""
echo "🛡️  Verificar AUTODEFESA no final do output para testes perigosos"
echo "======================================"

exit $EXIT_CODE
