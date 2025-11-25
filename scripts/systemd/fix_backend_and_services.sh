#!/bin/bash
set -euo pipefail

echo "🔧 Aplicando correções nos serviços OmniMind..."

# 1. Copiar serviços corrigidos
echo "1. Copiando serviços para /etc/systemd/system/..."
sudo cp /home/fahbrain/projects/omnimind/scripts/systemd/omnimind.service /etc/systemd/system/
sudo cp /home/fahbrain/projects/omnimind/scripts/systemd/omnimind-backend-direct.service /etc/systemd/system/omnimind-backend.service
echo "✅ Serviços copiados."

# 2. Recarregar daemon
echo "2. Recarregando daemon systemd..."
sudo systemctl daemon-reload
echo "✅ Daemon recarregado."

# 3. Verificar sintaxe
echo "3. Verificando sintaxe dos serviços..."
if sudo systemd-analyze verify /etc/systemd/system/omnimind.service; then
    echo "✅ omnimind.service OK."
else
    echo "❌ Erro de sintaxe no omnimind.service."
    exit 1
fi

if sudo systemd-analyze verify /etc/systemd/system/omnimind-backend.service; then
    echo "✅ omnimind-backend.service OK."
else
    echo "❌ Erro de sintaxe no omnimind-backend.service."
    exit 1
fi

# 4. Parar processos usando porta 8000
echo "4. Verificando processos na porta 8000..."
PORT_8000_PID=$(sudo lsof -t -i :8000 || true)
if [ -n "$PORT_8000_PID" ]; then
    echo "⚠️ Processo(s) usando porta 8000: PID(s) $PORT_8000_PID"
    echo "Parando processo(s)..."
    sudo kill -9 "$PORT_8000_PID" || true
    sleep 2
    echo "✅ Processo(s) parado(s)."
else
    echo "✅ Nenhum processo usando porta 8000."
fi

# 5. Reiniciar serviços
echo "5. Reiniciando serviços..."
sudo systemctl restart omnimind.service
sudo systemctl restart omnimind-backend.service
echo "✅ Serviços reiniciados."

# 6. Aguardar inicialização
echo "6. Aguardando inicialização (5s)..."
sleep 5

# 7. Verificar status
echo ""
echo "📊 Status dos Serviços:"
echo "======================="
sudo systemctl status omnimind.service --no-pager -l | head -n 15
echo ""
sudo systemctl status omnimind-backend.service --no-pager -l | head -n 15
echo ""
sudo systemctl status omnimind-mcp.service --no-pager -l | head -n 15

echo ""
echo "✅ Correções aplicadas!"
echo ""
echo "Para verificar portas:"
echo "  ss -tlnp | grep -E ':(8000|4321|4322|4323|4324|4325|4326)'"
echo ""
echo "Para testar backend:"
echo "  curl http://127.0.0.1:8000/health"

