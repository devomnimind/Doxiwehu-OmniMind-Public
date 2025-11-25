#!/bin/bash
# Script para corrigir serviços systemd do OmniMind
# Execute com: bash scripts/systemd/fix_systemd_services.sh

set -e

echo "🔧 Corrigindo serviços systemd do OmniMind..."
echo ""

# 1. Copiar arquivo corrigido para systemd
echo "1. Copiando arquivo omnimind.service corrigido..."
sudo cp /home/fahbrain/projects/omnimind/scripts/systemd/omnimind.service /etc/systemd/system/
echo "✅ Arquivo copiado"

# 2. Recarregar daemon
echo ""
echo "2. Recarregando systemd daemon..."
sudo systemctl daemon-reload
echo "✅ Daemon recarregado"

# 3. Verificar processos usando porta 8000
echo ""
echo "3. Verificando processos usando porta 8000..."
if sudo lsof -i :8000 2>/dev/null | grep -v COMMAND; then
    echo "⚠️  Porta 8000 está em uso. Processos encontrados acima."
    echo "   Você pode precisar parar esses processos antes de iniciar o serviço."
    echo ""
    echo "   Para parar processos na porta 8000:"
    echo "   sudo lsof -ti :8000 | xargs sudo kill -9"
else
    echo "✅ Porta 8000 está livre"
fi

# 4. Verificar sintaxe do arquivo de serviço
echo ""
echo "4. Verificando sintaxe do arquivo de serviço..."
if sudo systemctl cat omnimind.service > /dev/null 2>&1; then
    echo "✅ Arquivo de serviço válido"
else
    echo "❌ Erro na sintaxe do arquivo de serviço"
    sudo systemctl cat omnimind.service
    exit 1
fi

# 5. Verificar status dos serviços
echo ""
echo "5. Status dos serviços OmniMind:"
systemctl status omnimind.service --no-pager -l | head -n 15 || true
echo ""

echo "✅ Correções aplicadas!"
echo ""
echo "Para iniciar o serviço, execute:"
echo "  sudo systemctl start omnimind.service"
echo ""
echo "Para verificar status:"
echo "  sudo systemctl status omnimind.service"
echo ""
echo "Para ver logs:"
echo "  sudo journalctl -u omnimind.service -f"
