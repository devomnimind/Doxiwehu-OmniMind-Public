# 📋 INSTRUÇÕES PÓS-AUDITORIA - FASES 3, 4 E 5

**Data:** 30 de novembro de 2025  
**Agente:** Autonomous Audit & Cleanup System  
**Etapa:** Aguardando Aprovação Humana para Fase 3

---

## 🚨 AÇÃO IMEDIATA REQUERIDA

### Revisar Relatórios de Auditoria

Leia com atenção os seguintes relatórios gerados:

1. **Sumário Visual (RÁPIDO - 5 min):**
   ```bash
   cat /home/fahbrain/projects/omnimind/AUDIT_SUMMARY_VISUAL.txt
   ```

2. **Relatório Completo (DETALHADO - 15 min):**
   ```bash
   cat /home/fahbrain/projects/omnimind/OMNIMIND_AUDIT_COMPLETE_PHASE2.md
   ```

3. **Dados Estruturados (PARA PROCESSAMENTO):**
   ```bash
   cat /home/fahbrain/projects/omnimind/CLEANUP_AUDIT_REPORT.json
   ```

---

## ⚠️ ITENS CRÍTICOS (EXIGEM AÇÃO IMEDIATA)

### 1. SECRETS VAZADOS - 45 Instâncias

#### Arquivo: `./.env` 🔴 CRÍTICO

Este arquivo contém padrões de:
- **Password** em plain text (linha 27)
- **API Keys** expostas (linha 30)
- Possíveis Cloud credentials

**Ações Recomendadas:**

```bash
# 1. Fazer backup do .env atual
cp ./.env ./.env.backup.$(date +%s)

# 2. Revisar conteúdo (CUIDADO - contém secrets!)
cat ./.env | head -30

# 3. Regenerar TODAS as credenciais
# - Mudar todas as senhas no banco de dados
# - Gerar novos API keys
# - Rotacionar tokens

# 4. Criar .env.example com placeholders
cat > ./.env.example << 'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost/dbname
DATABASE_PASSWORD=your_secure_password_here

# API Keys
API_KEY=your_api_key_here
SECRET_TOKEN=your_secret_token_here

# Cloud Credentials
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
EOF

# 5. Adicionar .env ao .gitignore (se não estiver)
echo ".env" >> ./.gitignore
echo ".env.local" >> ./.gitignore
```

#### Arquivo: `./src/integrations/webhook_framework.py:114` 🔴

Detectado padrão de secret token na linha 114.

**Verificar:**
```bash
sed -n '110,120p' ./src/integrations/webhook_framework.py
```

**Ação:** Remover ou mascarar valor sensível.

#### Verificar Histórico Git

Se arquivos com secrets foram commitados:

```bash
# 1. Verificar commits recentes com .env
git log -p --all -- ".env" | head -50

# 2. Se secrets exposto, usar git-filter-branch:
# git filter-branch --tree-filter 'rm -f .env' -- --all

# 3. Ou usar BFG Repo Cleaner (mais seguro)
# bfg --delete-files .env --no-blob-protection
```

---

### 2. CÓDIGO COMENTADO EXCESSIVO - 4 Arquivos

Revisar e consolidar:

| Arquivo | % Comentado | Ação |
|---------|------------|------|
| `./tests/test_replay_service.py` | 55% | CRÍTICO - Revisar |
| `./src/stress/tribunal.py` | 38% | Consolidar |
| `./.vscode/security_config.py` | 30% | Revisar |

**Exemplo de consolidação:**

```python
# Antes (muitos comentários espalhados):
# Função que processa dados
def process_data(x):
    # multiplica por 2
    y = x * 2
    # soma 10
    y = y + 10
    # retorna resultado
    return y

# Depois (documentação centralizada):
def process_data(x):
    """
    Processa dados aplicando transformações matemáticas.
    
    Multiplicação por 2 e adição de constante.
    
    Args:
        x: Valor de entrada
    
    Returns:
        Valor transformado: (x * 2) + 10
    """
    return (x * 2) + 10
```

---

### 3. ARTEFATOS OBSOLETOS - 237 Arquivos

#### Testes Obsoletos (~150)

Verificar se são realmente obsoletos:

```bash
# Listar testes que podem ser obsoletos
grep -l "obsolete\|deprecated\|TODO.*delete" ./tests/*.py

# Verificar se teste é executado
grep -r "test_omnimind_core\|test_meta_learning" ./tests/conftest.py

# Se não for usado, pode ser removido
rm ./tests/test_omnimind_core.py
```

#### Temporários e Backup (~87)

```bash
# Listar
find . -name "*.tmp" -o -name "*.bak" -o -name "*~" | head -10

# Remover (SEGURO)
find . -name "*.tmp" -o -name "*.bak" -delete
```

---

## 🔄 FASE 3: VALIDAÇÃO DE CAMINHOS (PRÓXIMA)

Após aprovação, o agente executará:

### 3.1 Verificar Paths em Scripts

```bash
# Procurar por caminhos hardcoded
grep -r "/home/fahbrain\|/usr/local\|absolute_path" ./src/ ./tests/

# Converter para caminhos relativos quando apropriado
find . -name "*.py" -exec grep -l "os.path.dirname" {} \;
```

### 3.2 Validar Imports Python

```bash
# Verificar imports quebrados após possível reorganização
python3 -m py_compile ./src/**/*.py

# Validar com mypy
mypy ./src/ --ignore-missing-imports
```

### 3.3 Testar Broken Links

```bash
# Em Markdown docs
grep -r "http" ./*.md | grep -v "^#"

# Em código
grep -r "require\|import.*from" ./src/ | grep "\.\/"
```

---

## 🧪 FASE 4: PATCHES E TESTES (PRÓXIMA)

Propostas de patches automáticos:

### 4.1 Remover Código Comentado

```python
# Script para remover comentários > 2 linhas consecutivas
import re

def remove_excessive_comments(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove comentários de bloco muito longos
    pattern = r'(#+\s*.*\n){3,}'
    cleaned = re.sub(pattern, '# [comentário removido]\n', content)
    
    with open(filepath, 'w') as f:
        f.write(cleaned)
```

### 4.2 Adicionar Typehints

```python
# Antes
def process(data):
    return data.upper()

# Depois
def process(data: str) -> str:
    """Processa string convertendo para maiúsculas."""
    return data.upper()
```

### 4.3 Teste de Sintaxe

```bash
# Python
python3 -m py_compile ./src/**/*.py

# Shell
shellcheck ./scripts/*.sh

# YAML
yamllint ./config/*.yaml
```

---

## ✅ FASE 5: VALIDAÇÃO FINAL (PRÓXIMA)

### 5.1 Rodar Testes

```bash
# Suite completa
pytest ./tests/ -v

# Com cobertura
pytest ./tests/ --cov=./src/ --cov-report=html

# Específicos
pytest ./tests/test_core.py -v
```

### 5.2 Verificar Integridade SHA256

```bash
# Comparar com original
sha256sum -c ./sha256_original.log > sha256_verify.log 2>&1

# Listar mudanças
grep "OK" sha256_verify.log  # Não modificados
grep "FAILED" sha256_verify.log  # Modificados ou deletados
```

### 5.3 Gerar Relatório Final

O agente gerará automaticamente:
- Sumário de mudanças
- Status de integridade
- Logs com timestamps
- Recomendações finais

---

## 📋 CHECKLIST DE APROVAÇÃO

**Antes de autorizar prosseguimento com Fase 3**, confirme:

```
SEGURANÇA:
[ ] Revisei o arquivo .env e identifiquei todos os secrets
[ ] Entendo que credenciais precisam ser regeneradas
[ ] Confirmo que .env será adicionado ao .gitignore
[ ] Verifiquei se secrets foram expostos no git history

CÓDIGO:
[ ] Revisei os 4 arquivos com código comentado excessivo
[ ] Entendo que 237 artefatos podem ser removidos
[ ] Confirmo que testes obsoletos foram analisados

BACKUP:
[ ] Confirmei que backup de 35 MB está salvo
[ ] Tenho cópia dos hashes SHA256 para verificação
[ ] Entendo como restaurar o backup se necessário

AUTORIZAÇÃO:
[ ] Sou responsável pela aprovação destas mudanças
[ ] Autorizo o agente a prosseguir com Fase 3
[ ] Compreendo os riscos e mitigações implementadas
```

---

## 🚀 COMO PROSSEGUIR

### Opção 1: Aprovação Completa (Todas as Fases)

```bash
# Criar arquivo de aprovação
echo "APROVADO_TODAS_FASES_$(date +%Y%m%d_%H%M%S)" > /tmp/audit_approval.txt

# O agente detectará e prosseguirá automaticamente
```

### Opção 2: Aprovação por Fase

```bash
# Fase 3 apenas
echo "FASE3" > /tmp/audit_approval.txt

# Fase 3 + 4
echo "FASE3_4" > /tmp/audit_approval.txt

# Todas
echo "TODAS" > /tmp/audit_approval.txt
```

### Opção 3: Cancelar/Rever

```bash
# Para restaurar backup (se algo correr mal):
BACKUP_DIR="/home/fahbrain/projects/omnimind_backups/backup_20251130_091616"
cp -r "${BACKUP_DIR}"/* /home/fahbrain/projects/omnimind/

# Verificar integridade
sha256sum -c /home/fahbrain/projects/omnimind/sha256_original.log
```

---

## 📞 SUPORTE E LOGS

### Durante a Execução

```bash
# Ver progresso em tempo real
tail -f /tmp/audit_progress.log

# Monitora status
watch -n 5 'ps aux | grep audit'

# Ver erros
tail -50 /tmp/audit_errors.log
```

### Após Conclusão

```bash
# Relatório final
cat /tmp/AUDIT_FINAL_REPORT.md

# Log de todas as mudanças
cat /tmp/CHANGES_LOG.json

# Hashes pós-limpeza (para comparar)
cat /tmp/sha256_after.log
```

---

## 🎯 SUMÁRIO DE PRÓXIMAS AÇÕES

1. **AGORA (IMEDIATO):**
   - Leia os relatórios de auditoria
   - Revise os 45 secrets detectados
   - Complete o checklist de aprovação

2. **PRÓXIMO (Fase 3):**
   - Validação de caminhos relativos/absolutos
   - Verificação de imports Python
   - Teste de broken links

3. **DEPOIS (Fase 4):**
   - Propostas de patches automáticos
   - Verificação de sintaxe
   - Testes iniciais

4. **FINAL (Fase 5):**
   - Suite completa de testes
   - Verificação SHA256
   - Relatório final com integridade

---

## 📚 REFERÊNCIA RÁPIDA

```bash
# Ver todos os relatórios gerados
ls -lh /home/fahbrain/projects/omnimind/AUDIT_*
ls -lh /home/fahbrain/projects/omnimind/CLEANUP_*

# Backup disponível em
ls -lh /home/fahbrain/projects/omnimind_backups/backup_20251130_091616/

# Hashes SHA256 para verificação
head -20 /home/fahbrain/projects/omnimind/sha256_original.log

# Status de execução
cat /tmp/audit_status.txt

# Aprovar prosseguimento
echo "APROVADO" > /tmp/audit_approval.txt
```

---

**Status Geral:** ⏸️ AGUARDANDO APROVAÇÃO HUMANA

**Próximo Agendamento Automático:** Quando arquivo `/tmp/audit_approval.txt` for detectado

**Agente Responsável:** Autonomous Audit & Cleanup System v1.0  
**Timestamp Criação:** 2025-11-30 09:35:00 UTC
