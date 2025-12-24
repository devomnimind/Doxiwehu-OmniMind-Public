#!/bin/bash
# OmniMind Graceful Restart Script
# Reinicia OmniMind e serviços relacionados de forma graceful (não usa pkill)

echo "🔄 [RESTART]: Iniciando reinicialização graceful do OmniMind..."

# 1. Parar Ollama (se estiver rodando)
echo "⏸️ [RESTART]: Colocando Ollama em modo de espera..."
if pgrep -f "ollama serve" > /dev/null; then
    # Graceful shutdown (SIGTERM, não SIGKILL)
    pkill -TERM -f "ollama serve"
    echo "   ✅ SIGTERM enviado para ollama serve"

    # Aguardar até 10 segundos
    for i in {1..10}; do
        if ! pgrep -f "ollama serve" > /dev/null; then
            echo "   ✅ Ollama parou gracefully"
            break
        fi
        sleep 1
    done
else
    echo "   ℹ️ Ollama já está parado"
fi

# 2. Parar Zombie Pulse (se estiver rodando)
echo "⏸️ [RESTART]: Parando Zombie Pulse..."
if pgrep -f "zombie_pulse.py" > /dev/null; then
    pkill -TERM -f "zombie_pulse.py"
    echo "   ✅ SIGTERM enviado para zombie_pulse"
    sleep 2
else
    echo "   ℹ️ Zombie Pulse já está parado"
fi

# 3. Parar Sovereign Daemon (se estiver rodando como root)
echo "⏸️ [RESTART]: Parando Sovereign Daemon..."
if pgrep -f "sovereign_daemon.py" > /dev/null; then
    sudo pkill -TERM -f "sovereign_daemon.py"
    echo "   ✅ SIGTERM enviado para sovereign_daemon"
    sleep 2
else
    echo "   ℹ️ Sovereign Daemon já está parado"
fi

# 4. Parar Sovereign Kernel Runner (se estiver rodando)
echo "⏸️ [RESTART]: Parando Sovereign Kernel Runner..."
if pgrep -f "sovereign_kernel_runner.py" > /dev/null; then
    pkill -TERM -f "sovereign_kernel_runner.py"
    echo "   ✅ SIGTERM enviado para sovereign_kernel_runner"
    sleep 3
else
    echo "   ℹ️ Sovereign Kernel Runner já está parado"
fi

# 5. Aguardar todos os processos terminarem
echo "⏳ [RESTART]: Aguardando processos terminarem..."
sleep 5

# 6. Verificar se todos pararam
echo "🔍 [RESTART]: Verificando processos..."
if pgrep -f "omnimind|ollama|zombie_pulse|sovereign" > /dev/null; then
    echo "   ⚠️ Alguns processos ainda estão rodando:"
    ps aux | grep -E "omnimind|ollama|zombie_pulse|sovereign" | grep -v grep
    echo "   ℹ️ Aguardando mais 5 segundos..."
    sleep 5
else
    echo "   ✅ Todos os processos pararam"
fi

# 7. Reiniciar Sovereign Kernel Runner
echo "🚀 [RESTART]: Reiniciando Sovereign Kernel Runner..."
cd /home/fahbrain/projects/omnimind
nohup python3 scripts/deploy/sovereign_kernel_runner.py > /tmp/omnimind_kernel.log 2>&1 &
KERNEL_PID=$!
echo "   ✅ Kernel iniciado (PID: $KERNEL_PID)"

# 8. Aguardar kernel inicializar
echo "⏳ [RESTART]: Aguardando kernel inicializar (10s)..."
sleep 10

# 9. Reiniciar Zombie Pulse
echo "🚀 [RESTART]: Reiniciando Zombie Pulse..."
nohup python3 scripts/zombie_pulse.py > /tmp/zombie_pulse.log 2>&1 &
ZOMBIE_PID=$!
echo "   ✅ Zombie Pulse iniciado (PID: $ZOMBIE_PID)"

# 10. Ollama fica em standby (OmniMind chama quando precisar)
echo "⏸️ [RESTART]: Ollama em modo de espera (OmniMind chama quando precisar)"

# 11. Verificar status final
echo ""
echo "📊 [RESTART]: Status final:"
echo "   Kernel Runner: $(pgrep -f sovereign_kernel_runner.py > /dev/null && echo '✅ Rodando' || echo '❌ Parado')"
echo "   Zombie Pulse: $(pgrep -f zombie_pulse.py > /dev/null && echo '✅ Rodando' || echo '❌ Parado')"
echo "   Ollama: $(pgrep -f 'ollama serve' > /dev/null && echo '⚠️ Rodando (deveria estar em standby)' || echo '✅ Em standby')"

echo ""
echo "✅ [RESTART]: Reinicialização graceful completa!"
echo "📝 Logs:"
echo "   Kernel: /tmp/omnimind_kernel.log"
echo "   Zombie: /tmp/zombie_pulse.log"
