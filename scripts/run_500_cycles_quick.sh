#!/bin/bash

# Configuração de Ambiente
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export OMNIMIND_ENV="validation"

echo "=================================================="
echo "⚡ OMNIMIND QUICK VALIDATION (500 Cycles)"
echo "=================================================="

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="logs/validation_500_${TIMESTAMP}.log"
mkdir -p logs

echo "📜 Logs serão salvos em: $LOG_FILE"

# Executar wrapper de treinamento leve
# Usando o mesmo script robusto, mas com parâmetros reduzidos
# Redirecionando output para arquivo E terminal (tee)
python3 scripts/science_validation/run_extended_training.py \
    --cycles 500 \
    --interval 0.1 \
    --validation-interval 50 2>&1 | tee "$LOG_FILE"

RET_CODE=${PIPESTATUS[0]} # Captura o exit code do python, não do tee

echo "=================================================="
if [ $RET_CODE -eq 0 ]; then
    echo "✅ Validação Rápida Concluída com Sucesso (Exit Code 0)"
    echo "Verdadeiro Teste de Fogo: O sistema consentiu?"
    echo "Verifique logs para ver se a Membrana foi ativada."
elif [ $RET_CODE -eq 1 ]; then
    echo "🛑 Validação CIENTIFICAMENTE REJEITADA (Exit Code 1)"
    echo "O sistema completou o ciclo, mas os resultados foram rejeitados pela supervisão científica."
    echo "Verifique 'VEREDITO' no final do log."
elif [ $RET_CODE -eq 2 ]; then
    echo "⚠️ Validação APROVADA COM RESTRIÇÕES (Exit Code 2)"
    echo "O sistema foi aprovado, mas com ressalvas (CONDITIONAL)."
elif [ $RET_CODE -eq 137 ]; then
    echo "💀 Processo Morto pelo Sistema (OOM Killer / SIGKILL - Exit Code 137)"
    echo "Provável falta de memória. Tente fechar IDEs ou reduzir batch size."
elif [ $RET_CODE -eq 143 ]; then
    echo "🛑 Processo Interrompido pelo Usuário (SIGTERM - Exit Code 143)"
else
    echo "💥 FALHA CRÍTICA / CRASH (Exit Code $RET_CODE)"
    echo "O script terminou abruptamente. Pode ser Segfault (139) ou outro erro de sistema."
    echo "Verifique se 'Terminado' apareceu acima (indicativo de kill externo)."
fi
echo "=================================================="
