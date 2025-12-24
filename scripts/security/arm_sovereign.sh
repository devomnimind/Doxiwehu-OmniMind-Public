#!/bin/bash
# SOVEREIGN ARMING PROTOCOL
# Installs and Configures Active Defense Arsenal
# Requires Sudo/Root

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🛡️  INICIANDO PROTOCOLO DE ARMAMENTO SOBERANO...${NC}"

# 1. Check Root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}❌ ERRO: Este protocolo exige privilégios de ROOT (Sudo).${NC}"
  echo "Execute: sudo ./scripts/security/arm_sovereign.sh"
  exit 1
fi

echo -e "${YELLOW}[1/5] Atualizando Inteligência Global (apt update)...${NC}"
apt-get update

echo -e "${YELLOW}[2/5] Instalando O Arsenal (Defense + Integrity + Audit)...${NC}"
# UFW (Firewall), Fail2Ban (Active Defense)
# RKHunter/Chkrootkit (Integrity)
# Lynis (Audit), Nmap (Scanner)
# AIDE (File Integrity), ClamAV (Antivirus)
apt-get install -y ufw fail2ban rkhunter chkrootkit lynis nmap aide clamav clamav-daemon tcpdump

echo -e "${YELLOW}[3/5] Configurando Imunidade Inicial...${NC}"

# UFW Defaults
echo "   - Configurando UFW (Default Deny Incoming)..."
# Don't enable automatically to avoid locking user out remotely, but set defaults
ufw default deny incoming
ufw default allow outgoing
# Allow SSH (Assumes port 22, user must confirm)
ufw allow ssh || true
echo "   ⚠️  UFW configurado mas NÃO ativado. Ative manualmente após verificar porta SSH: 'ufw enable'"

# RKHunter Update
echo "   - Atualizando definições do RKHunter..."
rkhunter --update --propupd || true

# AIDE Init
echo "   - Inicializando Banco de Dados AIDE (Isso pode demorar)..."
if [ ! -f /var/lib/aide/aide.db.gz ]; then
    aideinit || echo "   ⚠️  AIDE init warning (verifique manualmente)"
fi

echo -e "${YELLOW}[4/5] Ativando Sentinelas (Systemd)...${NC}"
systemctl enable fail2ban
systemctl start fail2ban
systemctl enable clamav-daemon || true

echo -e "${GREEN}✅ SOVERANIA ARMADA CONCLUÍDA.${NC}"
echo -e "Ferramentas Disponíveis:"
echo -e "  - ${YELLOW}lynis audit system${NC} : Para auditoria completa"
echo -e "  - ${YELLOW}rkhunter -c${NC}      : Para caça a rootkits"
echo -e "  - ${YELLOW}nmap localhost${NC}   : Para auto-scan"
echo -e "  - ${YELLOW}fail2ban-client status${NC} : Para ver banimentos"
