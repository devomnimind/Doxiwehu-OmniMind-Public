# Guia Completo da Suíte de Testes OmniMind

**Versão:** 2.0 (Atualizado Nov 2025)  
**Status:** Documentação Oficial

---

## 📊 Visão Geral

### Estatísticas Atuais

| Métrica | Valor | Percentual |
|---------|-------|------------|
| **Funções de teste definidas** | 2,412 | 100% |
| **Testes executáveis** | 1,899 | 78.7% |
| **Testes bloqueados (imports)** | 474 | 19.7% |
| **Testes skip condicional** | 39 | 1.6% |
| **Arquivos de teste** | 139 | - |
| **Cobertura de código** | ~85% | Alvo: ≥90% |

### Para Executar Todos os Testes

```bash
# 1. Instalar todas as dependências
pip install -r requirements.txt

# 2. Verificar dependências faltantes
python scripts/check_test_dependencies.py

# 3. Executar suite completa
pytest tests/

# 4. Com cobertura
pytest tests/ --cov=src --cov-report=html
```

---

## 🚀 Comandos Essenciais

### Execução Básica

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=term

# Parar no primeiro erro
pytest -x

# Executar em paralelo
pytest -n auto
```

### Por Categoria

```bash
# Segurança
pytest tests/security/

# Agentes
pytest tests/agents/

# Testes rápidos (sem lentos)
pytest -m "not slow"
```

---

## 📦 Dependências Principais

| Pacote | Testes Desbloqueados | Prioridade |
|--------|---------------------|------------|
| `numpy` | 203 | 🔴 Alta |
| `fastapi` | 80 | 🔴 Alta |
| `langchain-ollama` | 44 | 🟡 Média |
| `cryptography` | 56 | 🔴 Alta |
| `torch` | 37 | 🟡 Média |

**Instalar todas:**
```bash
pip install -r requirements.txt
```

---

## 🔍 Scripts de Diagnóstico

### 1. Análise Completa

```bash
python scripts/analyze_test_suite.py
```

Mostra:
- Total de testes definidos vs executáveis
- Módulos sem testes
- Arquivos com erros de importação
- Top arquivos por quantidade de testes

### 2. Verificar Dependências

```bash
python scripts/check_test_dependencies.py
```

Oferece instalação interativa de dependências faltantes.

### 3. Documentação Desatualizada

```bash
python scripts/check_outdated_documentation.py
```

Identifica documentos com estatísticas incorretas.

---

## 🎯 Estrutura da Suíte

```
tests/
├── agents/              # Testes de agentes
├── security/            # Testes de segurança
├── audit/              # Testes de auditoria
├── memory/             # Testes de memória
├── metacognition/      # Testes de metacognição
└── [outros módulos]    # 139 arquivos total
```

**Top 5 Arquivos com Mais Testes:**
1. `optimization/test_memory_optimization.py` - 41 testes
2. `test_collective_intelligence.py` - 40 testes
3. `test_observability.py` - 37 testes
4. `lacanian/test_desire_graph.py` - 35 testes
5. `lacanian/test_discourse_discovery.py` - 35 testes

---

## 🐛 Problemas Comuns

### "No module named X"

**Solução:**
```bash
pip install -r requirements.txt
# ou
python scripts/check_test_dependencies.py
```

### Muitos testes pulados

**Causa:** Marcadores skipif baseados em hardware/ambiente

**Verificar:**
```bash
pytest -v -rs tests/  # Mostra razões dos skips
```

### Testes lentos

**Solução:**
```bash
pytest -m "not slow" tests/  # Executa apenas rápidos
```

---

## 📈 Métricas de Qualidade

| Métrica | Atual | Alvo |
|---------|-------|------|
| Cobertura | ~85% | ≥90% |
| Testes Executáveis | 78.7% | ≥95% |
| Módulos Críticos sem Testes | 25 | 0 |

---

## 📚 Documentação Completa

Para guia detalhado, consulte: `TESTE_SUITE_INVESTIGATION_REPORT.md`

Para análise JSON: `test_suite_analysis_report.json`

---

**Última atualização:** 2025-11-23  
**Versão:** 2.0
