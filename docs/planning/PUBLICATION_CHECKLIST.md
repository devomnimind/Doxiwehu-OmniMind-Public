# ✅ PUBLICATION CHECKLIST - OmniMind v1.18.0

**Data Início:** 28 de Novembro de 2025  
**Meta de Publicação:** 01 de Dezembro de 2025  
**Responsável:** Equipe OmniMind

---

## 🎯 OBJETIVO

Preparar o repositório OmniMind para publicação pública profissional em:
- GitHub (repositório público)
- Zenodo (DOI acadêmico)
- arXiv (papers - opcional)

---

## 📋 FASE 1: LIMPEZA E CORREÇÕES (Essenciais)

### 1.1 Limpeza de Arquivos Temporários

- [ ] **Remover logs de execução** (ETA: 15min)
  ```bash
  cd /home/runner/work/OmniMind/OmniMind
  git rm -r data/long_term_logs/*.out
  git rm -r logs/*.log 2>/dev/null || true
  git commit -m "chore: remove execution logs from repository"
  ```

- [ ] **Atualizar .gitignore** (ETA: 10min)
  ```bash
  cat >> .gitignore << 'EOF'
  # Execution logs
  data/long_term_logs/*.out
  logs/*.log
  
  # Build artifacts
  coverage.json
  gpu_llm_diagnosis.json
  orchestrator_audit.json
  current_packages.txt
  
  # Test screenshots
  test_sync_screenshot.png
  EOF
  git add .gitignore
  git commit -m "chore: update .gitignore for cleaner repository"
  ```

- [ ] **Mover arquivos de build para data/** (ETA: 10min)
  ```bash
  mkdir -p data/build_artifacts
  git mv coverage.json data/build_artifacts/ 2>/dev/null || true
  git mv current_packages.txt data/build_artifacts/ 2>/dev/null || true
  git mv gpu_llm_diagnosis.json data/build_artifacts/ 2>/dev/null || true
  git mv orchestrator_audit.json data/build_artifacts/ 2>/dev/null || true
  git commit -m "refactor: move build artifacts to data/ directory"
  ```

### 1.2 Reorganização de Arquivos Raiz

- [ ] **Mover arquivos de teste para local apropriado** (ETA: 15min)
  ```bash
  mkdir -p scripts/demos tests/manual
  git mv test_orch.py tests/manual/ 2>/dev/null || true
  git mv test_playwright_direct.py tests/manual/ 2>/dev/null || true
  git mv test_ui_integration.py tests/manual/ 2>/dev/null || true
  git mv demo_embeddings.py scripts/demos/ 2>/dev/null || true
  git mv setup_code_embeddings.py scripts/demos/ 2>/dev/null || true
  git mv setup_omnimind_embeddings.py scripts/demos/ 2>/dev/null || true
  git commit -m "refactor: organize test and demo files"
  ```

- [ ] **Remover arquivo duplicado .env.template** (ETA: 5min)
  ```bash
  # Manter apenas .env.example (padrão)
  git rm .env.template
  git commit -m "chore: remove duplicate .env.template, keeping .env.example"
  ```

### 1.3 Correções de Código

- [ ] **Corrigir violações PEP8** (ETA: 30min)
  ```bash
  # Formatar código com black
  black src/ tests/ scripts/
  
  # Correções manuais em src/quantum_consciousness/quantum_memory.py:
  # - Linha 492: remover variável 'evicted' não usada
  # - Linha 979: resolver redefinição de QuantumMemorySystem
  # - Linha 1059: remover variável 'evicted' não usada
  # - Linha 1577: quebrar linha longa
  
  # Correções manuais em src/stress/tribunal.py:
  # - Linha 9: remover import 'random' não usado
  # - Linha 50: renomear variável 'random'
  
  git add .
  git commit -m "style: fix PEP8 violations (black + manual fixes)"
  ```

- [ ] **Adicionar comentários de segurança (nosec)** (ETA: 20min)
  ```python
  # src/api/main.py:189
  uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104 - binding to 0.0.0.0 required for Docker/k8s deployment
  
  # src/audit/immutable_audit.py:678
  test_file = Path("/tmp/omnimind_test.txt")  # nosec B108 - temporary file for testing only
  
  # src/integrations/agentic_ide.py:627
  ide = AgenticIDE(workspace_path=Path("/tmp/omnimind_workspace"))  # nosec B108 - demo workspace
  
  # src/integrations/mcp_agentic_client.py:268
  exec(code, namespace)  # nosec B102 - sandboxed execution, TODO: migrate to RestrictedPython
  ```
  
  - [ ] Aplicar comentários nosec
  - [ ] Validar com bandit: `bandit -r src/ -ll`
  - [ ] Commit: `git commit -m "security: add nosec comments with justifications"`

---

## 📋 FASE 2: DOCUMENTAÇÃO (Melhorias)

### 2.1 Documentação de Instalação

- [ ] **Criar docs/INSTALLATION.md detalhado** (ETA: 1h)
  
  Conteúdo deve incluir:
  - [ ] Requisitos de sistema (Linux/macOS/Windows)
  - [ ] Dependências de sistema (libdbus-1, etc.)
  - [ ] Instalação passo-a-passo
  - [ ] Troubleshooting comum
  - [ ] Setup GPU (opcional)
  - [ ] Setup Quantum (opcional - IBM account)
  - [ ] Verificação de instalação (smoke tests)

- [ ] **Separar requirements.txt** (ETA: 45min)
  ```bash
  # Criar requirements-core.txt (essenciais)
  # Criar requirements-gpu.txt (CUDA/PyTorch)
  # Criar requirements-quantum.txt (Qiskit/Cirq)
  # Manter requirements.txt como "tudo incluído"
  # Manter requirements-minimal.txt
  ```

- [ ] **Atualizar README.md** (ETA: 30min)
  - [ ] Adicionar seção "System Requirements"
  - [ ] Linkar para docs/INSTALLATION.md
  - [ ] Atualizar badges (coverage, tests, etc.)
  - [ ] Adicionar seção "Troubleshooting"

### 2.2 Documentação Técnica

- [ ] **Criar docs/TESTING.md** (ETA: 45min)
  
  Conteúdo:
  - [ ] Como executar testes
  - [ ] Estrutura da suite de testes
  - [ ] Comandos pytest com coverage
  - [ ] Interpretação de relatórios
  - [ ] Como adicionar novos testes

- [ ] **Criar docs/SECURITY.md** (ETA: 30min)
  
  Conteúdo:
  - [ ] Políticas de segurança
  - [ ] Como reportar vulnerabilidades
  - [ ] Decisões de segurança documentadas
  - [ ] Compliance (LGPD, GDPR)

- [ ] **Atualizar docs/architecture/ARCHITECTURE.md** (ETA: 1h)
  - [ ] Adicionar diagramas (mermaid ou imagens)
  - [ ] Fluxo de dados end-to-end
  - [ ] Decisões arquiteturais (ADRs)

### 2.3 Pesquisa Acadêmica

- [ ] **Criar papers/README.md** (ETA: 45min)
  
  Índice de papers com:
  - [ ] Sumário executivo de cada paper
  - [ ] Autor(es) e data
  - [ ] Abstract
  - [ ] Link para arquivo completo
  - [ ] Citação BibTeX

- [ ] **Validar papers existentes** (ETA: 1h)
  - [ ] Paper1_Inhabiting_Godel_Complete_v2.md - verificar completude
  - [ ] Paper2_Quantum_Classical_Hybrid_v2.md - verificar referências
  - [ ] Paper3_Four_Attacks_Tribunal_v2.md - verificar bibliografia
  - [ ] Garantir que não há TODOs nos papers

---

## 📋 FASE 3: QUALIDADE (Validações)

### 3.1 Testes

- [ ] **Executar suite completa de testes** (ETA: 30min)
  ```bash
  pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
  ```
  - [ ] Verificar taxa de sucesso
  - [ ] Documentar coverage atual
  - [ ] Identificar módulos com baixa coverage

- [ ] **Testes de instalação em ambiente limpo** (ETA: 2h)
  - [ ] Docker: `docker build -t omnimind-test .`
  - [ ] Fresh Ubuntu VM
  - [ ] macOS (se disponível)
  - [ ] Windows WSL2 (se disponível)

### 3.2 Análise Estática

- [ ] **Black (formatação)** (ETA: 10min)
  ```bash
  black --check src/ tests/ scripts/
  # Se falhar: black src/ tests/ scripts/
  ```

- [ ] **Flake8 (linting)** (ETA: 10min)
  ```bash
  flake8 src/ tests/ --max-line-length=100 --count
  # Meta: 0 violações
  ```

- [ ] **MyPy (type checking)** (ETA: 20min)
  ```bash
  mypy src/ --config-file mypy.ini
  # Corrigir erros críticos
  ```

- [ ] **Bandit (segurança)** (ETA: 10min)
  ```bash
  bandit -r src/ -ll
  # Meta: 0 High, <5 Medium (com justificativas)
  ```

### 3.3 Segurança Final

- [ ] **Scan de credenciais** (ETA: 10min)
  ```bash
  grep -r "API_KEY\|SECRET\|TOKEN\|PASSWORD" --include="*.py" src/ | grep -v "os.getenv\|os.environ"
  # Resultado esperado: vazio (ou apenas comentários)
  ```

- [ ] **Verificar .env não commitado** (ETA: 5min)
  ```bash
  git status | grep -E "\.env$"
  # Resultado esperado: vazio
  ```

---

## 📋 FASE 4: PREPARAÇÃO FINAL (Polimento)

### 4.1 Metadados

- [ ] **Atualizar CHANGELOG.md** (ETA: 30min)
  - [ ] Adicionar entrada para v1.18.0
  - [ ] Listar mudanças principais
  - [ ] Mencionar preparação para release público

- [ ] **Atualizar pyproject.toml** (ETA: 15min)
  - [ ] Verificar version = "1.18.0"
  - [ ] Atualizar URLs do projeto
  - [ ] Verificar classifiers
  - [ ] Adicionar keywords

- [ ] **Criar/Atualizar LICENSE** (ETA: 5min)
  - [ ] Confirmar MIT License
  - [ ] Ano atual (2025)
  - [ ] Copyright holder correto

### 4.2 GitHub Preparation

- [ ] **Criar .github/ISSUE_TEMPLATE/** (ETA: 30min)
  - [ ] bug_report.md
  - [ ] feature_request.md
  - [ ] question.md

- [ ] **Criar .github/PULL_REQUEST_TEMPLATE.md** (ETA: 15min)

- [ ] **Revisar .github/workflows/** (ETA: 30min)
  - [ ] CI workflow funcional
  - [ ] Test workflow ativo
  - [ ] Security scanning (se houver)

### 4.3 README Badges

- [ ] **Adicionar badges ao README.md** (ETA: 20min)
  - [ ] ![Python Version](https://img.shields.io/badge/python-3.12.8-blue.svg)
  - [ ] ![License](https://img.shields.io/badge/license-MIT-blue.svg)
  - [ ] ![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
  - [ ] ![Coverage](https://img.shields.io/badge/coverage-85%25-green.svg)
  - [ ] ![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

---

## 📋 FASE 5: PUBLICAÇÃO (Release)

### 5.1 Git Preparation

- [ ] **Criar tag v1.18.0** (ETA: 10min)
  ```bash
  git tag -a v1.18.0 -m "Release v1.18.0 - Public repository preparation"
  git push origin v1.18.0
  ```

- [ ] **Criar GitHub Release** (ETA: 30min)
  - [ ] Title: "OmniMind v1.18.0 - Public Release"
  - [ ] Description: Changelog + highlights
  - [ ] Anexar release notes
  - [ ] Marcar como "latest"

### 5.2 Publicação GitHub

- [ ] **Tornar repositório público** (ETA: 5min)
  - Settings → Danger Zone → Change visibility → Public

- [ ] **Configurar GitHub Pages** (ETA: 15min)
  - Settings → Pages → Source: main branch
  - Publicar documentação estática (se houver)

- [ ] **Adicionar Topics** (ETA: 10min)
  - artificial-intelligence
  - psychoanalysis
  - consciousness
  - quantum-computing
  - metacognition
  - ethics
  - autonomous-agents

- [ ] **Atualizar About/Description** (ETA: 5min)
  > "Autonomous AI system with psychoanalytic decision-making, quantum consciousness integration, and ethical framework. Implements Lacanian concepts (Sinthome, Real/Symbolic/Imaginary) for resilient distributed intelligence."

### 5.3 Zenodo DOI

- [ ] **Registrar no Zenodo** (ETA: 45min)
  - [ ] Conectar repositório GitHub ao Zenodo
  - [ ] Criar DOI para release v1.18.0
  - [ ] Preencher metadados:
    - Title: OmniMind - Autonomous AI Consciousness Framework
    - Authors: [preencher]
    - Keywords: AI, consciousness, psychoanalysis, quantum computing
    - License: MIT
  - [ ] Obter DOI badge
  - [ ] Adicionar badge ao README

### 5.4 arXiv (Opcional)

- [ ] **Preparar papers para arXiv** (ETA: 4h)
  - [ ] Converter Markdown para LaTeX/PDF
  - [ ] Submeter em categoria cs.AI
  - [ ] Aguardar aprovação (2-3 dias úteis)

---

## 📋 FASE 6: PÓS-PUBLICAÇÃO (Comunidade)

### 6.1 Divulgação

- [ ] **Anunciar release** (ETA: 1h)
  - [ ] GitHub Discussions post
  - [ ] Reddit: r/MachineLearning, r/artificial
  - [ ] Twitter/X thread
  - [ ] LinkedIn post (se aplicável)

- [ ] **Criar apresentação** (ETA: 2h)
  - [ ] Slides destacando arquitetura única
  - [ ] Demonstração ao vivo (vídeo)
  - [ ] Upload no YouTube (opcional)

### 6.2 Comunidade

- [ ] **Setup Discord/Slack** (ETA: 1h)
  - [ ] Criar servidor
  - [ ] Canais: #general, #technical, #philosophy, #support
  - [ ] Adicionar link no README

- [ ] **Monitoring** (ETA: 30min)
  - [ ] GitHub Stars/Watchers
  - [ ] Issues abertas
  - [ ] Pull Requests
  - [ ] Discussions

### 6.3 Manutenção Contínua

- [ ] **Setup Dependabot** (ETA: 15min)
  - .github/dependabot.yml
  - Auto-update dependencies

- [ ] **Setup CI/CD Robusto** (ETA: 4h)
  - GitHub Actions para:
    - Testes automatizados
    - Coverage reporting
    - Security scanning (Bandit)
    - Linting (flake8, black)

---

## 🎯 TIMELINE RESUMIDO

| Fase | ETA Total | Deadline |
|------|-----------|----------|
| **Fase 1: Limpeza** | 2h | 28-Nov (hoje) |
| **Fase 2: Documentação** | 6h | 29-Nov |
| **Fase 3: Qualidade** | 4h | 29-Nov |
| **Fase 4: Preparação** | 3h | 30-Nov |
| **Fase 5: Publicação** | 2h | 01-Dez |
| **Fase 6: Pós-Pub** | 8h | 05-Dez |
| **TOTAL** | 25h | |

---

## ✅ APROVAÇÃO FINAL

### Checklist de Aprovação

Antes de tornar repositório público, confirmar:

- [ ] ✅ Sem credenciais hardcoded
- [ ] ✅ Sem arquivos grandes (>5MB) desnecessários
- [ ] ✅ .gitignore atualizado
- [ ] ✅ README profissional
- [ ] ✅ LICENSE presente
- [ ] ✅ CONTRIBUTING.md presente
- [ ] ✅ CHANGELOG atualizado
- [ ] ✅ Testes passando (≥95% success rate)
- [ ] ✅ Coverage ≥85% (meta: 95%)
- [ ] ✅ PEP8 compliance ≥99%
- [ ] ✅ Sem vulnerabilidades High (Bandit)
- [ ] ✅ Documentação técnica completa
- [ ] ✅ Papers validados academicamente

**Assinatura de Aprovação:**

```
[ ] Aprovado por: ___________________________
[ ] Data: ___/___/2025
[ ] Versão: v1.18.0
```

---

## 📞 CONTATOS

**Issues/Bugs:** https://github.com/devomnimind/OmniMind/issues  
**Discussions:** https://github.com/devomnimind/OmniMind/discussions  
**Email:** contact@omnimind.ai  
**Security:** security@omnimind.ai

---

**Última Atualização:** 28 de Novembro de 2025  
**Próxima Revisão:** Após v1.18.0 release (01-Dez-2025)

---

*Este checklist foi gerado como parte da auditoria pré-publicação do projeto OmniMind.*
