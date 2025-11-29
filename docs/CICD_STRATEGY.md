# 🚀 CI/CD Strategy - GitHub Actions Workflow Configuration

**Data**: 29 de novembro de 2025  
**Versão**: v1.17.8  
**Status**: ✅ Implementado

---

## 📋 Problema Identificado

### Situação Anterior
```
❌ CI.yml falha por tamanho dos testes
❌ Timeout de 6 horas em testes muito pesados
❌ Não usa pytest-timeout configurado
❌ Sem separação de responsabilidades
❌ Sem qualidade de código validada
```

### Causa Raiz
- Testes de quantum, ML e benchmarks executam em GitHub Actions
- Sem exclusão de testes lentos/heavy
- Sem limite de tempo por teste
- Sem estratégia de qualidade de código separada

---

## ✅ Solução Implementada

### Estratégia em 3 Camadas

```
┌─────────────────────────────────────────────────────────────┐
│ GitHub Actions - CI/CD Pipeline                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ ⚡ FAST TRACK (15 min) - EVERY PUSH                          │
│ ├─ quality.yml: Black, Flake8, MyPy, Bandit, Safety        │
│ └─ test-core.yml: Unit tests (no heavy)                     │
│                                                               │
│ 🌙 NIGHTLY (3 hours) - SCHEDULED 2 AM UTC                   │
│ └─ test-full.yml: All tests (quantum, ml, benchmarks)       │
│                                                               │
│ 🔄 ORCHESTRATOR                                              │
│ └─ ci-pipeline.yml: Coordinates fast track + summary        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Workflows Criados

### 1. **quality.yml** ⚡ (15 min)
**Propósito**: Validação de código sem executar testes

```yaml
Triggers: Toda push/PR
Timeout: 15 minutos
Verificações:
  ✅ Black (formatação)
  ✅ isort (ordenação de imports)
  ✅ Flake8 (linting)
  ✅ MyPy (type checking)
  ✅ Bandit (segurança)
  ✅ Safety (vulnerabilidades conhecidas)
```

**Quando falha**: Bloqueia merge
**Como corrigir**:
```bash
black src tests                          # Formatar
isort src tests                          # Ordenar imports
flake8 src tests --max-line-length=100   # Revisar erros de linting
mypy src tests --ignore-missing-imports  # Type check
```

---

### 2. **test-core.yml** 🧪 (25 min)
**Propósito**: Testes unitários principais sem overhead

```yaml
Triggers: Toda push/PR
Timeout: 25 minutos (30 segundos por teste)
Executa:
  ✅ tests/ (exceto quantum, ml, heavy)
  ✅ tests/consciousness/ (sem @pytest.mark.slow)
Exclui:
  ❌ tests/quantum_ai/
  ❌ tests/quantum_consciousness/
  ❌ tests/benchmarks/
  ❌ tests/stress/
  ❌ tests/load_tests/
  ❌ Testes marcados como @slow
```

**Timeout**: 30 segundos por teste (configurado no pytest.ini)
**Como corrigir testes que falham**:
```bash
# Rodar localmente com mesmo timeout
pytest tests/ --timeout=30 -m "not slow" -v
```

---

### 3. **test-full.yml** 🌙 (180 min)
**Propósito**: Validação completa (nightly)

```yaml
Triggers:
  - Agendado: Toda noite 2 AM UTC
  - Manual: workflow_dispatch
  - Mudanças: Em arquivos quantum/ml
Timeout: 180 minutos (3 horas)
Executa: Todos os testes (incluindo quantum, ml, benchmarks)
Gera: Coverage reports completos
```

**Quando falha**: Log salvo em artifacts (não bloqueia main)
**Para executar manualmente**: GitHub Actions → test-full.yml → Run workflow

---

### 4. **ci-pipeline.yml** 🔄 (Orchestrator)
**Propósito**: Coordena workflows e gera sumário

```yaml
Triggers: Toda push/PR
Executora:
  → quality.yml (paralelo)
  → test-core.yml (espera quality.yml)
  → summary (espera ambas)
Tempo Total: ~40 minutos (sequential fast track)
```

---

## 🚀 Como Funciona

### Fluxo de um PR

```
1. PR Aberto
   ↓
2. GitHub Actions Dispara ci-pipeline.yml
   ├─ quality.yml (Black, Flake8, MyPy) → 15 min
   └─ test-core.yml (espera quality) → 25 min
   ↓
3. Resultado em ~40 minutos
   ├─ Se ✅ PASS: Pronto para merge
   └─ Se ❌ FAIL: Bloqueia merge (revisar logs)
```

### Fluxo Noturno

```
2 AM UTC (toda noite)
   ↓
test-full.yml dispara
   ├─ Todos os testes (3 horas)
   ├─ Coverage completo
   └─ Artifacts salvos (30 dias)
```

---

## 📊 Comparação: Antes vs Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Tempo PR** | 6 horas (timeout) ❌ | 40 minutos ✅ |
| **Qualidade Código** | Não validava | Validado (Black, Flake8, MyPy) ✅ |
| **Testes Rápidos** | Misturados com lentos | Separados ✅ |
| **Teste Lentos** | Falhava em PR | Nightly schedule ✅ |
| **Coverage** | Não completo | Nightly completo ✅ |
| **Bloqueador** | Sim (6 horas) ❌ | Rápido (40 min) ✅ |
| **Timeout por Teste** | Não configurado | 30 segundos ✅ |

---

## 🛠️ Configurações Técnicas

### pytest.ini - Já Configurado
```ini
[pytest]
addopts = --timeout=30
```
✅ Garante que nenhum teste rode indefinidamente

### requirements-core.txt
```
pytest
pytest-cov
pytest-timeout  ← Essencial
```
✅ Instalado em test-core.yml

### requirements-ci.txt
```
black
flake8
isort
mypy
pylint
bandit
safety
```
✅ Instalado em quality.yml

---

## ❌ Como Corrigir Falhas

### Se quality.yml falha

**Black (Formatação)**
```bash
black src tests
git add .
git commit -m "style: format code with black"
```

**Flake8 (Linting)**
```bash
flake8 src tests --max-line-length=100 --show-source
# Revisar e corrigir erros manualmente
```

**MyPy (Type Checking)**
```bash
mypy src tests --ignore-missing-imports --show-error-codes
# Adicionar type hints conforme necessário
```

### Se test-core.yml falha

**Rodar localmente**
```bash
# Mesmo que CI roda
pytest tests/ --timeout=30 -m "not slow" -v

# Se teste específico falha
pytest tests/path/to/test.py -v --timeout=30
```

**Se é timeout (> 30s)**
```bash
# Marcar como @pytest.mark.slow
# ou reduzir ciclos de teste
```

---

## 📈 Métricas e Monitoramento

### Actions Tab no GitHub
```
Abre: https://github.com/devomnimind/OmniMind/actions
Mostra:
  • Status de cada workflow
  • Tempo de execução
  • Logs detalhados
  • Artifacts (reports, coverage)
```

### Artifacts Gerados

**Em Cada PR (test-core)**
- `pytest_core.log` - Saída dos testes
- `htmlcov/` - Cobertura de código (HTML)

**Nightly (test-full)**
- `pytest_full.log` - Saída completa
- `coverage.json` - Cobertura em JSON
- `htmlcov/` - Cobertura HTML completa
- Retidos por 30 dias

---

## 🔒 Segurança

### Secrets Necessários
```
OMNIMIND_QDRANT_CLOUD_URL
OMNIMIND_QDRANT_API_KEY
OMNIMIND_QDRANT_COLLECTION
OMNIMIND_QDRANT_VECTOR_SIZE
```
✅ Não usados em quality.yml (não necessário)
✅ Usados apenas em test-full.yml se disponíveis

### Branch Protection Rules Recomendadas
```
Require status checks to pass:
  ✅ Code Quality - Fast Quality Checks
  ✅ Core Unit Tests
```
→ Impede merge sem passar em quality + core tests

---

## 🚀 Próximos Passos

### 1. Ativar Workflows
```bash
# No repositório, eles já estão criados
# Apenas fazer push para ativar
git add .github/workflows/
git commit -m "ci: implement optimized ci/cd pipeline"
git push origin master
```

### 2. Configurar Branch Protection
```
GitHub Settings → Branches → Add Rule
  • Branch name pattern: master
  • Require status checks: quality.yml + test-core.yml
  • Require branches up to date
```

### 3. Monitorar Primeiro PR
- Abrir PR simples
- Verificar workflows em ~40 minutos
- Confirmar que bloqueia/passa corretamente

### 4. Agendar Nightly
- Workflow test-full.yml já está agendado
- Verifica cronômetro em Actions → Scheduled

---

## 📝 Estrutura de Commits Esperada

```
Commit com mudança de código:
  ↓
quality.yml dispara (15 min)
  → Black ✅
  → Flake8 ✅
  → MyPy ✅
  ↓
test-core.yml dispara (25 min)
  → Unit tests ✅
  ↓
PR pronto para merge (40 min total)
```

---

## ✅ Checklist de Implementação

- ✅ quality.yml criado
- ✅ test-core.yml criado
- ✅ test-full.yml criado
- ✅ ci-pipeline.yml criado
- ✅ pytest-timeout instalado
- ✅ pytest.ini com --timeout=30
- ✅ requirements-ci.txt com ferramentas
- ✅ Documentação completa

---

## 🎯 Benefícios

1. **⚡ Rápido**: PR validado em ~40 minutos (vs 6+ horas)
2. **🎯 Focado**: Qualidade separada de testes pesados
3. **🛡️ Seguro**: Bloqueia merge se falhar
4. **📊 Transparente**: Logs e reports detalhados
5. **🌙 Completo**: Validação full nightly sem impacto PR
6. **🔍 Debugável**: Testes com timeout evita hangs
7. **📈 Escalável**: Fácil adicionar mais workflows

---

## 📞 Referências

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Timeout Plugin](https://pytest-timeout.readthedocs.io/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [MyPy Type Checking](https://mypy.readthedocs.io/)

---

**Versão**: v1.17.8  
**Status**: ✅ **IMPLEMENTADO E PRONTO**

Todos os workflows estão configurados no repositório público.
Próximo passo: Fazer push e verificar Actions tab no GitHub.

