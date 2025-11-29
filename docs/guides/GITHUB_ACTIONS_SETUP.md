# 🚀 GitHub Actions Setup Guide

## O Problema

O workflow SonarQube precisa de credenciais (SONAR_TOKEN) para funcionar. Essas credenciais **NÃO podem ser commitadas** no repositório público.

## A Solução: Usar Secrets + .env

### 🎯 Estratégia

1. **Repositório Público** (`devomnimind/OmniMind`)
   - `.env.example` ✅ (template com placeholders - PÚBLICO)
   - `.env` ❌ (arquivo real com credenciais - PRIVADO, em .gitignore)
   - Workflow lê variáveis de `.env` para testes locais

2. **GitHub Actions** (CI/CD Remoto)
   - Usa **Repository Secrets** em vez de `.env`
   - Seguro: Secrets são criptografados pelo GitHub
   - Visível apenas para você

3. **Desenvolvedor Local**
   - Copia `.env.example` para `.env`
   - Preenche com suas credenciais reais
   - `.env` fica local (nunca commitado)

---

## 📋 Passo-a-Passo para Configurar

### Passo 1: Obter SONAR_TOKEN

```bash
# 1. Acesse SonarCloud
https://sonarcloud.io/account/security

# 2. Crie um novo token ("Generate Tokens")
# 3. Copie o token gerado
```

### Passo 2: Adicionar Secret no GitHub

```bash
# No seu repositório GitHub:
Settings → Secrets and variables → Actions → New repository secret

Name: SONAR_TOKEN
Value: [seu_token_copiado_do_sonarcloud]

# Repita para outros secrets se necessário:
# GITHUB_TOKEN (já fornecido automaticamente pelo GitHub)
```

### Passo 3: Configurar Localmente

```bash
cd /home/fahbrain/projects/omnimind

# Copiar template
cp .env.example .env

# Editar .env com seus valores reais
vim .env
# ou
nano .env
```

Arquivo `.env` deve ficar assim:

```bash
# OmniMind - Environment Configuration
SONAR_TOKEN=squ_xxxxxxxxxxxxx_your_real_token_xxxxx
SONAR_HOST_URL=https://sonarcloud.io
SONAR_PROJECT_KEY=devomnimind_OmniMind
SONAR_ORGANIZATION=devomnimind
GITHUB_TOKEN=ghp_xxxxx_your_github_token_xxxxx
OMNIMIND_DEV_MODE=true
DEBUG=false
```

### Passo 4: Carregar Variáveis (Shell)

```bash
# Ativar variáveis de ambiente
source .env

# Verificar que foram carregadas
echo $SONAR_TOKEN

# Ou adicionar ao seu ~/.zshrc/.bashrc para ser automático
echo "source /path/to/omnimind/.env" >> ~/.zshrc
source ~/.zshrc
```

### Passo 5: Executar Workflow Localmente

```bash
# Com variáveis carregadas
make validate

# Ou manualmente
pytest tests/ -v --cov=src

# Para SonarQube local (se tiver sonar-scanner):
sonar-scanner \
  -Dsonar.projectKey=devomnimind_OmniMind \
  -Dsonar.organization=devomnimind \
  -Dsonar.sources=src/ \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=$SONAR_TOKEN
```

---

## 🔐 Segurança

### ✅ O que ESTÁ seguro

- `.env.example`: Público, sem valores reais ✅
- `.env`: Privado, em `.gitignore`, nunca commitado ✅
- `Repository Secrets`: Criptografados pelo GitHub ✅
- Workflow: Lê secrets automaticamente ✅

### ❌ O que NÃO fazer

```bash
# ❌ NUNCA faça isto:
echo "SONAR_TOKEN=squ_xxxxx" > .env  # Deixar commitado
git add .env                          # Adicionar ao repo
export SONAR_TOKEN=squ_xxxxx          # Usar em shell scripts

# ✅ FAÇA ASSIM:
cp .env.example .env                  # Usar template
source .env                           # Carregar arquivo
# .env fica local, nunca é commitado
```

---

## 📊 Verificação

Para confirmar que está funcionando:

```bash
# 1. Verificar que .env está ignorado
git status | grep -i ".env"
# Resultado esperado: .env não aparece (está em .gitignore)

# 2. Verificar que .env.example está tracked
git status | grep ".env.example"
# Resultado esperado: arquivo pode estar staged/untracked

# 3. Verificar variáveis carregadas
source .env
echo "SONAR_TOKEN=$SONAR_TOKEN"
echo "SONAR_ORG=$SONAR_ORGANIZATION"
```

---

## 🚀 Fluxo Completo

### Local (Desenvolvedor)

```
┌─────────────────────────────────┐
│ 1. Clone repositório            │
│    git clone ...                │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 2. Copiar .env.example → .env   │
│    cp .env.example .env         │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 3. Preencher .env com credenciais
│    (SONAR_TOKEN, etc)           │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 4. Carregar variáveis           │
│    source .env                  │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 5. Executar testes              │
│    pytest tests/ -v --cov=src   │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 6. Fazer commit (SEM .env)      │
│    git commit -m "..."          │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 7. Push para GitHub             │
│    git push origin master       │
└─────────────────────────────────┘
```

### Remote (GitHub Actions)

```
┌─────────────────────────────────┐
│ 1. Webhook acionado (push)      │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 2. GitHub Actions dispara       │
│    sonarqube-audit.yml          │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 3. Carrega Repository Secrets   │
│    ${{ secrets.SONAR_TOKEN }}   │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 4. Executa workflow com secrets │
│    (mesmo que .env local)       │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 5. Gera relatórios              │
│    Coverage, SonarQube, etc.    │
└────────────┬────────────────────┘
             │
┌────────────v────────────────────┐
│ 6. Upload de artefatos          │
│    reports/, htmlcov/, etc.     │
└─────────────────────────────────┘
```

---

## 📝 Checklist Final

- [ ] Você tem conta SonarCloud (https://sonarcloud.io)
- [ ] Você gerou um SONAR_TOKEN
- [ ] Você adicionou SONAR_TOKEN ao GitHub Secrets
- [ ] Você copiou `.env.example` para `.env`
- [ ] Você preencheu `.env` com suas credenciais
- [ ] Você rodou `source .env` no seu shell
- [ ] Você verificou que `.env` está em `.gitignore`
- [ ] Você fez `git status` e `.env` NÃO aparece
- [ ] Você pode rodar tests localmente: `pytest tests/ -v`
- [ ] Workflow no GitHub Actions rodar com sucesso

---

## 🆘 Troubleshooting

### Problema: "SONAR_TOKEN not found"

```bash
# Solução 1: Verificar se .env foi carregado
echo $SONAR_TOKEN

# Solução 2: Carregar manualmente
source .env
echo $SONAR_TOKEN

# Solução 3: Verificar se .env existe
ls -la .env
```

### Problema: "Permission denied" ao executar workflow

```bash
# Solução: GitHub Secrets não têm permissão de escrita
# Use apenas secrets para LEITURA
# Para escrita, adicione outputs no workflow
```

### Problema: Tests falham localmente

```bash
# Verificar se variáveis estão carregadas
env | grep SONAR

# Se não aparecerem:
source .env
env | grep SONAR

# Deve mostrar suas credenciais
```

---

## 📚 Referências

- [SonarCloud Tokens](https://sonarcloud.io/account/security)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [GitHub Actions Environment Variables](https://docs.github.com/en/actions/learn-github-actions/environment-variables)
- [.env file best practices](https://12factor.net/config)

---

## ✨ Resumo

| Arquivo | Visibilidade | Propósito |
|---------|------|---------|
| `.env.example` | ✅ Público | Template com placeholders |
| `.env` | ❌ Privado | Credenciais reais (em .gitignore) |
| GitHub Secrets | ❌ Privado | Credenciais para CI/CD |
| Workflow `.yml` | ✅ Público | Lógica de teste (sem secrets) |

**Resultado**: Máxima segurança + total transparência! 🔐✨
