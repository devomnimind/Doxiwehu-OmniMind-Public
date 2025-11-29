# 📜 SCRIPTS - OmniMind Automation Scripts

**Data:** 29 de novembro de 2025
**Versão:** 1.18.0

## 🎯 INSTALAÇÃO DE SERVIÇOS SYSTEMD

### ✅ RECOMENDADO: Script Principal
```bash
# Instala TODOS os serviços corretamente
sudo ./scripts/systemd/install_all_services.sh
```

**Serviços instalados:**
- `omnimind.service` - Backend principal (porta 8000)
- `omnimind-daemon.service` - Daemon autônomo
- `omnimind-frontend.service` - Frontend web (porta 3000)
- `omnimind-mcp.service` - Servidores MCP
- `omnimind-qdrant.service` - Banco vetorial

### ❌ DESATUALIZADO: Não usar
```bash
# DEPRECATED - Instala serviço conflitante
./scripts/install_systemd_services.sh  # ❌ NÃO USAR
```

**Por que não usar:** Instala `omnimind-backend.service` que conflita com `omnimind.service`.

## 🧹 LIMPEZA DE SERVIÇOS DUPLICADOS

```bash
# Remove serviços conflitantes
sudo ./scripts/systemd/cleanup_duplicate_services.sh
```

## 🔧 SCRIPTS DE MANUTENÇÃO

### Correção de Serviços
```bash
# Corrige configurações de serviços
sudo ./scripts/systemd/fix_all_services.sh
```

### Instalação de Produção
```bash
# Setup completo para produção
sudo ./scripts/production/install_systemd.sh
```

## 📋 STATUS DOS SERVIÇOS

```bash
# Ver status de todos os serviços
systemctl status omnimind.service omnimind-daemon.service omnimind-frontend.service omnimind-mcp.service omnimind-qdrant.service

# Ver logs
sudo journalctl -u omnimind.service -f
```

## ⚠️ IMPORTANTE

- **Nunca instale** `omnimind-backend.service` - foi removido por causar conflitos
- **Sempre use** `omnimind.service` como serviço principal
- **Execute limpeza** se houver conflitos: `cleanup_duplicate_services.sh`

---

**Última atualização:** 29/11/2025