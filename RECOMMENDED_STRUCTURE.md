# 🏗️ RECOMMENDED STRUCTURE - OmniMind Public Repository

**Data:** 28 de Novembro de 2025  
**Versão:** 1.18.0  
**Objetivo:** Estrutura ideal para repositório público profissional

---

## 📂 ESTRUTURA RECOMENDADA

### Visão Hierárquica Completa

```
omnimind/
├── .github/                          # GitHub-specific configs
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── question.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── workflows/
│   │   ├── ci.yml                   # Continuous Integration
│   │   ├── ci-light.yml             # Fast CI (smoke tests)
│   │   ├── security.yml             # Security scanning
│   │   └── tests.yml                # Full test suite
│   ├── dependabot.yml
│   ├── CODEOWNERS
│   └── copilot-instructions.md
│
├── audit/                            # Audit reports
│   ├── README.md                    # Index of audits
│   ├── 1_INVENTORY.md
│   ├── 2_CODE_QUALITY.md
│   ├── 3_ARCHITECTURE.md
│   ├── 4_FUNCIONALIDADES.md
│   ├── 7_INCONSISTENCIAS.md
│   ├── 8_OPORTUNIDADES.md
│   └── AUDITORIA_CONSOLIDADA.md
│
├── config/                           # Configuration files
│   ├── agent_config.yaml
│   ├── agent_identity.yaml
│   ├── ethics.yaml
│   ├── metacognition.yaml
│   ├── omnimind.yaml
│   ├── security.yaml
│   ├── mcp_servers.json
│   ├── external_ai_providers.yaml
│   ├── hardware_profile.json
│   ├── systemd/
│   │   ├── omnimind-backend.service
│   │   └── omnimind-frontend.service
│   ├── redis/
│   │   └── redis-cluster.conf
│   └── linting/
│       └── .yamllint
│
├── data/                             # Data directory (mostly gitignored)
│   ├── .gitkeep
│   ├── benchmarks/
│   ├── build_artifacts/              # 🆕 Moved from root
│   │   ├── coverage.json
│   │   ├── current_packages.txt
│   │   └── gpu_llm_diagnosis.json
│   ├── long_term_logs/
│   │   └── .gitkeep                 # Logs ignored in .gitignore
│   └── test_reports/
│       ├── coverage.json
│       ├── htmlcov/
│       └── pytest_output.log
│
├── datasets/                         # Test/demo datasets
│   └── [small datasets only]
│
├── deploy/                           # Deployment scripts
│   └── [deployment configurations]
│
├── docs/                             # Documentation
│   ├── README.md                    # Documentation index
│   ├── architecture/
│   │   ├── ARCHITECTURE.md          # Main architecture doc
│   │   ├── ADR/                     # Architecture Decision Records
│   │   └── diagrams/                # UML, C4, flowcharts
│   ├── api/
│   │   ├── API.md                   # API reference
│   │   └── endpoints/
│   ├── guides/
│   │   ├── INSTALLATION.md          # 🆕 Detailed installation
│   │   ├── QUICKSTART.md
│   │   ├── TESTING.md               # 🆕 Testing guide
│   │   ├── DEPLOYMENT.md
│   │   └── CONTRIBUTING_GUIDE.md
│   ├── philosophy/
│   │   ├── PHILOSOPHY.md
│   │   ├── LACANIAN_CONCEPTS.md
│   │   └── GLOSSARY.md              # 🆕 Terms glossary
│   ├── research/
│   │   ├── papers/                  # Academic papers
│   │   ├── audits/                  # Research audits
│   │   ├── reports/                 # Technical reports
│   │   └── bibliography.md          # 🆕 Central bibliography
│   ├── security/
│   │   └── SECURITY.md              # 🆕 Security policy
│   └── reports/
│       └── benchmarks/
│
├── k8s/                              # Kubernetes configs
│   └── [k8s manifests]
│
├── logs/                             # Logs directory (gitignored)
│   └── .gitkeep
│
├── notebooks/                        # Jupyter notebooks
│   ├── README.md                    # Notebooks index
│   └── [educational notebooks]
│
├── papers/                           # Academic papers (top-level)
│   ├── README.md                    # 🆕 Papers index with abstracts
│   ├── Paper1_Inhabiting_Godel_Complete_v2.md
│   ├── Paper2_Quantum_Classical_Hybrid_v2.md
│   ├── Paper3_Four_Attacks_Tribunal_v2.md
│   └── references/
│       └── bibliography.bib         # BibTeX citations
│
├── reports/                          # Generated reports
│   └── [auto-generated reports]
│
├── scripts/                          # Utility scripts
│   ├── README.md                    # Scripts documentation
│   ├── demos/                       # 🆕 Demo scripts (moved from root)
│   │   ├── demo_embeddings.py
│   │   ├── setup_code_embeddings.py
│   │   └── setup_omnimind_embeddings.py
│   ├── benchmarks/
│   │   ├── ibm_quantum_real_benchmark.py
│   │   └── benchmark_omnimind.py
│   ├── deployment/
│   │   └── deploy_huggingface.py
│   ├── systemd/
│   │   └── install_all_services.sh
│   ├── validation/
│   │   ├── validate_quantum_minimal.py
│   │   └── validate_quantum_strict.py
│   └── utilities/
│       └── [utility scripts]
│
├── src/                              # Source code
│   ├── __init__.py
│   ├── agents/                      # Multi-agent system
│   ├── api/                         # FastAPI backend
│   ├── architecture/
│   ├── attention/
│   ├── audit/                       # Audit system
│   ├── autopoietic/                 # Self-creation
│   ├── coevolution/                 # Human-AI co-evolution
│   ├── common/                      # Shared utilities
│   ├── compliance/                  # LGPD, GDPR
│   ├── consciousness/               # Consciousness modules
│   ├── daemon/                      # Background services
│   ├── decision_making/
│   ├── desire_engine/
│   ├── distributed/
│   ├── economics/
│   ├── embeddings/
│   ├── embodied_cognition/
│   ├── ethics/                      # Ethics system
│   ├── experiments/
│   ├── hibernation/
│   ├── identity/
│   ├── integrations/                # External integrations
│   ├── kernel_ai/
│   ├── lacanian/                    # Lacanian psychoanalysis
│   ├── learning/
│   ├── memory/                      # Memory systems
│   ├── meta_learning/
│   ├── metacognition/               # Metacognition levels
│   ├── metrics/
│   ├── motivation/
│   ├── multimodal/
│   ├── narrative_consciousness/
│   ├── neurosymbolic/
│   ├── observability/
│   ├── onboarding/
│   ├── optimization/
│   ├── orchestrator/                # Agent orchestration
│   ├── phenomenology/
│   ├── philosophy/
│   ├── polivalence/
│   ├── quantum_ai/
│   ├── quantum_consciousness/       # Quantum modules
│   ├── quantum_real/
│   ├── scaling/
│   ├── scars/                       # Scar integration
│   ├── security/
│   ├── services/
│   ├── sinthome/                    # Sinthome concept
│   ├── social/
│   ├── stress/                      # Stress testing
│   ├── swarm/                       # Swarm intelligence
│   ├── testing/
│   ├── tools/
│   ├── tribunal_do_diabo/           # Devil's Tribunal
│   ├── workflows/
│   └── phase16_integration.py
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest config
│   ├── manual/                      # 🆕 Manual tests (moved from root)
│   │   ├── test_orch.py
│   │   ├── test_playwright_direct.py
│   │   └── test_ui_integration.py
│   ├── agents/
│   ├── attention/
│   ├── audit/
│   ├── consciousness/
│   ├── ethics/
│   ├── integration/                 # Integration tests
│   ├── memory/
│   ├── quantum_consciousness/
│   ├── stress/
│   └── [mirrors src/ structure]
│
├── typings/                          # Type stubs
│   └── [type definitions]
│
├── web/                              # Frontend (React)
│   ├── package.json
│   ├── src/
│   ├── public/
│   └── README.md
│
├── .dockerignore
├── .env.example                     # 🔧 Only this (removed .env.template)
├── .flake8
├── .gitignore
├── .python-version
├── activate_venv.sh
├── AUDIT_REPORT.md                  # 🆕 Audit report
├── CHANGELOG.md
├── CLEANUP_LOG.md                   # 🆕 Cleanup log
├── CONTRIBUTING.md
├── Dockerfile.tests
├── FINAL_AUDIT_CERTIFICATION.md
├── FINAL_RECOMMENDATION.md          # 🆕 Final recommendation
├── LICENSE
├── METRICS_SUMMARY.md               # 🆕 Metrics summary
├── PUBLICATION_CHECKLIST.md         # 🆕 Publication checklist
├── README.md
├── RECOMMENDED_STRUCTURE.md         # 🆕 This file
├── ROADMAP.md
├── ROADMAP_PHASE_23_FUNDING.md
├── conftest.py
├── mypy.ini
├── prepare_public_repo.sh           # 🆕 Cleanup script
├── pyproject.toml
├── pytest.ini
├── pyrightconfig.json
├── requirements-benchmark.txt
├── requirements-ci.txt
├── requirements-cpu.txt
├── requirements-dev.txt
├── requirements-gpu.txt             # 🆕 Separated
├── requirements-minimal.txt
├── requirements-quantum.txt         # 🆕 Separated
├── requirements.lock
├── requirements.txt
├── sonar-project.properties
└── nginx-omnimind-proxy.conf
```

---

## 📝 MUDANÇAS PRINCIPAIS

### 🆕 Adições Recomendadas

1. **docs/guides/INSTALLATION.md** - Documentação detalhada de instalação
2. **docs/guides/TESTING.md** - Guia de testes
3. **docs/security/SECURITY.md** - Política de segurança
4. **docs/philosophy/GLOSSARY.md** - Glossário de termos
5. **papers/README.md** - Índice de papers com abstracts
6. **requirements-gpu.txt** - Dependências GPU separadas
7. **requirements-quantum.txt** - Dependências quantum separadas
8. **Documentos de auditoria** - AUDIT_REPORT.md, METRICS_SUMMARY.md, etc.

### 🔄 Reorganizações

#### Da Raiz → Novos Destinos

```
test_orch.py                    → tests/manual/
test_playwright_direct.py       → tests/manual/
test_ui_integration.py          → tests/manual/
demo_embeddings.py              → scripts/demos/
setup_code_embeddings.py        → scripts/demos/
setup_omnimind_embeddings.py    → scripts/demos/
coverage.json                   → data/build_artifacts/
current_packages.txt            → data/build_artifacts/
gpu_llm_diagnosis.json          → data/build_artifacts/
orchestrator_audit.json         → data/build_artifacts/
test_sync_screenshot.png        → [removido]
.env.template                   → [removido - manter só .env.example]
```

### ❌ Remoções

- Todos os logs em `data/long_term_logs/*.out`
- Cache Python (`__pycache__/`, `*.pyc`)
- Cache pytest (`.pytest_cache/`)
- Arquivos temporários (`*.tmp`, `*~`)

---

## 🎯 PRINCÍPIOS DE ORGANIZAÇÃO

### 1. Raiz Limpa
**Objetivo:** Apenas arquivos essenciais e de configuração

**Permitido:**
- README, LICENSE, CONTRIBUTING
- Arquivos de configuração (.flake8, pytest.ini, etc.)
- Arquivos de build (pyproject.toml, requirements.txt)
- Scripts de setup (activate_venv.sh)
- Documentação de alto nível (CHANGELOG, ROADMAP)

**Não Permitido:**
- Logs de execução
- Screenshots de teste
- Build artifacts
- Scripts de teste/demo

### 2. Separação de Responsabilidades

| Tipo de Conteúdo | Localização |
|-------------------|-------------|
| **Código Core** | `src/` |
| **Testes** | `tests/` |
| **Documentação** | `docs/` |
| **Papers** | `papers/` ou `docs/research/papers/` |
| **Scripts** | `scripts/` |
| **Configuração** | `config/` ou raiz |
| **Dados** | `data/` (gitignored) |
| **Logs** | `logs/` (gitignored) |
| **Build Artifacts** | `data/build_artifacts/` |

### 3. Espelhamento de Estruturas

**Princípio:** `tests/` deve espelhar `src/`

```
src/agents/orchestrator_agent.py
  ↓ corresponde a
tests/agents/test_orchestrator_agent.py
```

### 4. Documentação Próxima ao Código

**Princípio:** READMEs em subdiretórios para orientação local

```
scripts/
├── README.md              # Documentação de todos os scripts
├── demos/
│   └── README.md          # Documentação específica de demos
└── benchmarks/
    └── README.md          # Documentação de benchmarks
```

---

## 📦 ESTRUTURA DE REQUIREMENTS

### Separação Recomendada

```
requirements.txt              # Tudo incluído (instalação padrão)
requirements-core.txt         # Apenas essenciais (API, agents básicos)
requirements-gpu.txt          # PyTorch + CUDA (GPU acceleration)
requirements-quantum.txt      # Qiskit, Cirq (quantum computing)
requirements-dev.txt          # Ferramentas de desenvolvimento
requirements-ci.txt           # Para CI/CD
requirements-minimal.txt      # Mínimo para testes básicos
requirements-benchmark.txt    # Para benchmarking
requirements.lock             # Versões exatas (reproducibilidade)
```

### Dependências por Categoria

#### Core (Essenciais)
- Python 3.12.8
- FastAPI + Uvicorn
- Pydantic
- PyYAML
- Rich
- Structlog

#### AI/ML
- LangChain + LangGraph
- Transformers (Hugging Face)
- Sentence-Transformers

#### Storage
- Qdrant (vetores)
- Redis (cache/queue)
- Supabase (opcional)

#### GPU (Opcional)
- PyTorch 2.6.0+cu124
- CUDA 12.4+

#### Quantum (Opcional)
- Qiskit
- Google Cirq
- IBM Quantum (API)

#### Testing
- pytest + pytest-cov + pytest-asyncio

#### Quality
- black
- flake8
- mypy
- bandit
- radon

---

## 🔒 GITIGNORE RECOMENDADO

### Categorias Principais

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/
*.coverage.*
coverage.json
.tox/

# MyPy
.mypy_cache/
.dmypy.json
dmypy.json

# Logs
logs/*.log
data/long_term_logs/*.out
*.log

# Build Artifacts
coverage.json
gpu_llm_diagnosis.json
orchestrator_audit.json
current_packages.txt

# Environment
.env
.env.local

# Test Artifacts
test_*.png
test_sync_screenshot.png

# Temp Files
*.tmp
*~
Thumbs.db

# OS
.DS_Store
Thumbs.db
```

---

## 📚 DOCUMENTAÇÃO RECOMENDADA

### Estrutura docs/

```
docs/
├── README.md                    # Documentation hub
├── guides/
│   ├── INSTALLATION.md          # Step-by-step installation
│   ├── QUICKSTART.md            # 5-minute tutorial
│   ├── TESTING.md               # Running tests
│   ├── DEPLOYMENT.md            # Production deployment
│   ├── TROUBLESHOOTING.md       # Common issues
│   └── FAQ.md                   # Frequently asked questions
├── architecture/
│   ├── ARCHITECTURE.md          # High-level architecture
│   ├── ADR/                     # Architecture Decision Records
│   │   ├── 001-sinthome-concept.md
│   │   ├── 002-quantum-integration.md
│   │   └── ...
│   └── diagrams/                # Visual diagrams
│       ├── system_overview.png
│       ├── data_flow.mermaid
│       └── ...
├── api/
│   ├── API.md                   # Complete API reference
│   └── endpoints/
│       ├── agents.md
│       ├── memory.md
│       └── ...
├── philosophy/
│   ├── PHILOSOPHY.md            # Philosophical foundations
│   ├── LACANIAN_CONCEPTS.md     # Lacan for developers
│   ├── ETHICS.md                # Ethical framework
│   └── GLOSSARY.md              # Term definitions
├── research/
│   ├── papers/                  # Academic papers
│   ├── audits/                  # Technical audits
│   ├── reports/                 # Research reports
│   └── bibliography.md          # Citations
└── security/
    ├── SECURITY.md              # Security policy
    ├── VULNERABILITY_REPORT.md  # How to report
    └── COMPLIANCE.md            # LGPD, GDPR
```

---

## ✅ CHECKLIST DE CONFORMIDADE

### Verificação de Estrutura

- [ ] Raiz contém <25 arquivos
- [ ] Todos os testes em `tests/`
- [ ] Todos os scripts em `scripts/`
- [ ] Documentação em `docs/`
- [ ] Logs em `logs/` (gitignored)
- [ ] Build artifacts em `data/build_artifacts/`
- [ ] Configurações em `config/`
- [ ] Sem cache Python versionado
- [ ] Sem logs versionados
- [ ] Sem credenciais commitadas

### Verificação de Documentação

- [ ] README.md na raiz
- [ ] LICENSE presente
- [ ] CONTRIBUTING.md presente
- [ ] CHANGELOG.md atualizado
- [ ] docs/guides/INSTALLATION.md presente
- [ ] docs/guides/TESTING.md presente
- [ ] docs/security/SECURITY.md presente
- [ ] papers/README.md com índice

---

## 🎯 BENEFÍCIOS DA ESTRUTURA

### Para Desenvolvedores

1. **Navegação Intuitiva:** Encontrar arquivos rapidamente
2. **Separação Clara:** Código vs. testes vs. docs
3. **Escalabilidade:** Estrutura suporta crescimento
4. **Onboarding:** Novos contribuidores se orientam facilmente

### Para Usuários

1. **Documentação Acessível:** Guides na raiz de `docs/`
2. **Exemplos Claros:** Scripts de demo em `scripts/demos/`
3. **Instalação Simples:** Requirements separados por caso de uso

### Para Mantenedores

1. **Manutenibilidade:** Estrutura modular e organizada
2. **CI/CD Eficiente:** Testes bem organizados
3. **Auditabilidade:** Histórico claro em `audit/`
4. **Profissionalismo:** Impressão positiva para colaboradores

---

## 📋 PRÓXIMOS PASSOS

### Implementação

1. Executar `prepare_public_repo.sh`
2. Validar estrutura com checklist acima
3. Criar documentos faltantes (INSTALLATION.md, etc.)
4. Testar instalação em ambiente limpo
5. Commit e push: `git commit -m "refactor: implement recommended repository structure"`

---

**Estrutura criada por:** Agente de Auditoria e Preparação de Repositório  
**Data:** 28 de Novembro de 2025  
**Status:** RECOMENDAÇÃO OFICIAL

---

*Esta estrutura é baseada nas melhores práticas de projetos open-source de alto impacto e adaptada às necessidades específicas do OmniMind.*
