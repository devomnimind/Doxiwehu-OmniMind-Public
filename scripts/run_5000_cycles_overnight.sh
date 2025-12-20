#!/bin/bash
# Script para Execução Noturna de Treinamento Longo (5000 Ciclos)

# 1. Configurar Ambiente
export OMNIMIND_BACKEND_DEVICE="cpu"
export PYTHONFAULTHANDLER=1

echo "=================================================="
echo "🚀 OmniMind: Preparando Long Run (5000 Ciclos)"
echo "=================================================="
echo "✅ Backend Device: CPU (Economizando VRAM)"
echo "⚠️ Recomendação: Feche IDEs e navegadores pesados."
echo "=================================================="

# 2. Executar Indexador (Robusto) - Opcional, descomente se quiser rodar junto
# echo "📚 Atualizando Indexação de Livros..."
# ./.venv/bin/python3 scripts/indexing/library_indexer.py --paths "data/library_sources/free-livros" "/home/fahbrain/Downloads/Livros"

# 3. Executar Treinamento (Wrapper Robusto)
echo "🧠 Iniciando Ciclo de Treinamento (Estimativa: 4-6 horas)..."
./.venv/bin/python3 scripts/science_validation/robust_training_wrapper.py --cycles 5000 --interval 0.5

echo "=================================================="
echo "✅ Treinamento Finalizado."
echo "📊 Relatório salvo em data/test_reports/"
echo "=================================================="
