#!/bin/bash
# ============================================================================
# OMNIMIND PROCESS KILLER (Robust Tree Cleanup)
# ============================================================================
# Usage: ./kill_omnimind_tree.sh [pattern]
# Default pattern: "python3.*run_extended_training|library_indexer"

PATTERN="${1:-python3.*(run_extended_training|library_indexer|omnimind)}"

echo "🔍 Buscando processos matching: '$PATTERN'"

# Find PIDs
PIDS=$(pgrep -f "$PATTERN")

if [ -z "$PIDS" ]; then
    echo "✅ Nenhum processo encontrado."
    exit 0
fi

echo "⚠️  Processos encontrados (Pais): $PIDS"

# Function to kill tree
kill_tree() {
    local pid=$1
    local children=$(pgrep -P $pid)

    for child in $children; do
        kill_tree $child
    done

    echo "💀 Matando PID $pid ($(ps -p $pid -o comm=))"
    kill -9 $pid 2>/dev/null
}

for pid in $PIDS; do
    echo "🌳 Analisando árvore do PID $pid..."
    kill_tree $pid
done

# Force verify GPU cleanup
echo "🧹 Verificando GPU..."
ZOMBIE_GPU=$(nvidia-smi | grep "python" | awk '{print $5}')
if [ ! -z "$ZOMBIE_GPU" ]; then
    echo "☢️  Processos Zumbis na GPU detectados: $ZOMBIE_GPU"
    echo "🔪 Executando limpeza forçada na GPU..."
    echo "$ZOMBIE_GPU" | xargs -r kill -9
fi

echo "✅ Limpeza completa. Memória liberada."
ps aux | grep -E "$PATTERN" | grep -v grep
