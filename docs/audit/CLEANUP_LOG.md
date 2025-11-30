# 🗑️ CLEANUP LOG - Preparação OmniMind para Publicação

**Data:** 28 de Novembro de 2025  
**Versão:** 1.17.5 → 1.18.0  
**Objetivo:** Remover ruídos e preparar repositório para release público

---

## 📋 CATEGORIAS DE LIMPEZA

### 1. Logs de Execução (Removidos/A Remover)

#### data/long_term_logs/*.out
```
❌ data/long_term_logs/api_async_queue.out
❌ data/long_term_logs/api_clean.out
❌ data/long_term_logs/api_clean_start.out
❌ data/long_term_logs/api_daemon_monitor.out
❌ data/long_term_logs/api_final_restart.out
❌ data/long_term_logs/api_final_test.out
❌ data/long_term_logs/api_restart.out
❌ data/long_term_logs/api_safe_version.out
❌ data/long_term_logs/api_server.out
❌ data/long_term_logs/api_server_final.out
❌ data/long_term_logs/api_server_new.out
❌ data/long_term_logs/api_server_realmetrics.out
❌ data/long_term_logs/tribunal_intense.out
❌ data/long_term_logs/tribunal_monitor.out
```

**Razão:** Logs de execução não devem ser versionados  
**Ação:** `git rm data/long_term_logs/*.out` + adicionar ao .gitignore  
**Status:** ⏳ Pendente

#### Outros logs
```
❌ logs/*.log (se houver)
❌ *.log (arquivos raiz)
```

**Status:** ⏳ Pendente

---

### 2. Arquivos de Build/Análise (Mover ou Remover)

#### Raiz do Repositório
```
📦 coverage.json → data/build_artifacts/
📦 current_packages.txt → data/build_artifacts/
📦 gpu_llm_diagnosis.json → data/build_artifacts/
📦 orchestrator_audit.json → data/build_artifacts/
📦 feedback_report.txt → data/build_artifacts/
📦 log_analysis_test.json → data/build_artifacts/
```

**Razão:** Organização - build artifacts não devem estar na raiz  
**Ação:** `mkdir -p data/build_artifacts && git mv [files] data/build_artifacts/`  
**Status:** ⏳ Pendente

---

### 3. Arquivos de Teste no Diretório Raiz (Reorganizar)

```
🔄 test_orch.py → tests/manual/
🔄 test_playwright_direct.py → tests/manual/
🔄 test_ui_integration.py → tests/manual/
🔄 demo_embeddings.py → scripts/demos/
🔄 setup_code_embeddings.py → scripts/demos/
🔄 setup_omnimind_embeddings.py → scripts/demos/
```

**Razão:** Raiz deve conter apenas arquivos essenciais  
**Ação:** `git mv [files] [destino]`  
**Status:** ⏳ Pendente

#### Screenshots de Teste
```
❌ test_sync_screenshot.png
```

**Razão:** Screenshot de teste não deve ser versionado  
**Ação:** `git rm test_sync_screenshot.png` + adicionar ao .gitignore  
**Status:** ⏳ Pendente

---

### 4. Arquivos de Configuração Duplicados (Remover)

```
❌ .env.template (manter apenas .env.example)
```

**Razão:** Duplicação - padrão é .env.example  
**Ação:** `git rm .env.template`  
**Status:** ⏳ Pendente

---

### 5. Cache Python (Limpeza Automática)

```
❌ **/__pycache__/ (todos os diretórios)
❌ *.pyc
❌ *.pyo
```

**Razão:** Arquivos gerados automaticamente  
**Ação:** `find . -type d -name '__pycache__' -exec rm -rf {} +`  
**Status:** ⏳ Pendente (script automatizado)

---

### 6. Pytest/Coverage Cache (Limpeza)

```
❌ .pytest_cache/
❌ htmlcov/
❌ .coverage
```

**Razão:** Cache de ferramentas de teste  
**Ação:** `rm -rf .pytest_cache htmlcov .coverage`  
**Status:** ⏳ Pendente (script automatizado)

---

### 7. Arquivos Temporários (Limpeza)

```
❌ *.tmp
❌ *~
❌ .DS_Store (macOS)
❌ Thumbs.db (Windows)
```

**Razão:** Arquivos temporários do sistema  
**Ação:** `find . -name '*.tmp' -delete` (e similares)  
**Status:** ⏳ Pendente (script automatizado)

---

## ✅ ARQUIVOS MANTIDOS (Essenciais)

### Código Core
```
✅ src/ (toda a estrutura)
✅ tests/ (toda a estrutura)
✅ scripts/ (scripts utilitários)
```

### Documentação
```
✅ README.md
✅ CONTRIBUTING.md
✅ CHANGELOG.md
✅ ROADMAP.md
✅ ROADMAP_PHASE_23_FUNDING.md
✅ FINAL_AUDIT_CERTIFICATION.md
✅ docs/ (toda a estrutura)
✅ papers/ (toda a estrutura)
✅ audit/ (relatórios de auditoria)
```

### Configuração
```
✅ pyproject.toml
✅ pytest.ini
✅ mypy.ini
✅ .flake8
✅ .gitignore
✅ .python-version
✅ .dockerignore
✅ .env.example
✅ config/ (toda a estrutura)
```

### Deploy
```
✅ Dockerfile.tests
✅ docker-compose.yml (se houver)
✅ k8s/ (Kubernetes configs)
✅ deploy/ (deploy scripts)
```

### Outros Essenciais
```
✅ LICENSE
✅ requirements*.txt
✅ conftest.py
✅ activate_venv.sh
```

---

## 📊 RESUMO DE AÇÕES

### Por Tipo de Ação

| Ação | Quantidade | Arquivos |
|------|------------|----------|
| **Remover** | ~30 | Logs, cache, temporários |
| **Mover** | ~12 | Build artifacts, testes |
| **Manter** | ~900 | Código, docs, configs |

### Por Prioridade

| Prioridade | Ações | ETA |
|------------|-------|-----|
| **Alta** | Remover logs, credenciais | 30min |
| **Média** | Reorganizar raiz | 1h |
| **Baixa** | Limpeza cache | 15min |

**Total Estimado:** 1h 45min

---

## 🔧 COMANDOS DE EXECUÇÃO

### Script Automatizado (Recomendado)
```bash
# Dry-run (apenas visualizar)
./prepare_public_repo.sh --dry-run

# Executar limpeza
./prepare_public_repo.sh
```

### Manual (Passo-a-Passo)

#### 1. Remover Logs
```bash
git rm -r data/long_term_logs/*.out
git rm logs/*.log 2>/dev/null || true
git commit -m "chore: remove execution logs"
```

#### 2. Reorganizar Raiz
```bash
mkdir -p data/build_artifacts tests/manual scripts/demos

git mv coverage.json data/build_artifacts/
git mv current_packages.txt data/build_artifacts/
git mv gpu_llm_diagnosis.json data/build_artifacts/
git mv orchestrator_audit.json data/build_artifacts/

git mv test_orch.py tests/manual/
git mv test_playwright_direct.py tests/manual/
git mv test_ui_integration.py tests/manual/

git mv demo_embeddings.py scripts/demos/
git mv setup_code_embeddings.py scripts/demos/
git mv setup_omnimind_embeddings.py scripts/demos/

git rm test_sync_screenshot.png
git rm .env.template

git commit -m "refactor: reorganize repository structure"
```

#### 3. Atualizar .gitignore
```bash
cat >> .gitignore << 'EOF'

# Execution logs
data/long_term_logs/*.out
logs/*.log

# Build artifacts
coverage.json
*.json.tmp
gpu_llm_diagnosis.json
orchestrator_audit.json

# Test artifacts
test_*.png

# Cache
__pycache__/
.pytest_cache/
.mypy_cache/
htmlcov/
.coverage

# Temp files
*.tmp
*~
.DS_Store
Thumbs.db
EOF

git add .gitignore
git commit -m "chore: update .gitignore for cleaner repository"
```

#### 4. Limpeza de Cache (não versionado)
```bash
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
find . -name '*.pyc' -delete 2>/dev/null || true
find . -name '*.pyo' -delete 2>/dev/null || true
find . -name '*.tmp' -delete 2>/dev/null || true
find . -name '*~' -delete 2>/dev/null || true
rm -rf .pytest_cache htmlcov .coverage .mypy_cache
```

---

## ✅ VERIFICAÇÃO PÓS-LIMPEZA

### Checklist

- [ ] Nenhum arquivo *.out versionado
- [ ] Nenhum arquivo *.log versionado
- [ ] Raiz contém apenas arquivos essenciais
- [ ] .gitignore atualizado
- [ ] git status limpo (ou apenas mudanças intencionais)
- [ ] Nenhum cache Python versionado

### Comandos de Verificação

```bash
# Verificar logs
git ls-files | grep -E '\.(out|log)$'
# Resultado esperado: vazio

# Verificar raiz
ls -la | grep -E '^-' | wc -l
# Resultado esperado: ~15-20 arquivos essenciais

# Verificar .gitignore funcionando
git status --ignored
# Verificar que logs e cache estão ignorados
```

---

## 📈 IMPACTO DA LIMPEZA

### Antes da Limpeza
- **Tamanho:** 36 MB
- **Arquivos versionados:** ~950
- **Ruído:** ~40 arquivos temporários/desnecessários

### Depois da Limpeza (Estimado)
- **Tamanho:** ~34 MB (-5%)
- **Arquivos versionados:** ~910 (-4%)
- **Ruído:** 0 arquivos desnecessários

### Benefícios

1. **Clareza:** Repositório mais fácil de navegar
2. **Performance:** Git operations mais rápidas
3. **Profissionalismo:** Primeira impressão positiva
4. **Manutenção:** Menor confusão sobre o que é essencial

---

## 📝 NOTAS IMPORTANTES

### O Que NÃO Será Removido

- ✅ Relatórios de auditoria (audit/)
- ✅ Benchmarks históricos (ibm_results/)
- ✅ Notebooks educacionais (notebooks/)
- ✅ Datasets de teste (datasets/) - se pequenos
- ✅ Documentação completa (docs/, papers/)

### Arquivos Grandes (>5MB)

**Resultado da Busca:** Nenhum arquivo >5MB encontrado ✅

Se houver arquivos grandes no futuro:
- Considerar Git LFS para modelos/datasets
- Ou mover para release assets no GitHub

---

## 🔄 REVERSÃO (Se Necessário)

### Desfazer Últimas Mudanças

```bash
# Desfazer último commit (mantém mudanças locais)
git reset --soft HEAD~1

# Desfazer mudanças locais também
git reset --hard HEAD~1

# Recuperar arquivo específico
git checkout HEAD~1 -- <caminho/do/arquivo>
```

### Backup Antes de Começar

```bash
# Criar branch de backup
git checkout -b backup-pre-cleanup
git checkout main

# Se precisar reverter tudo
git checkout backup-pre-cleanup
git branch -D main
git checkout -b main
```

---

## ✅ APROVAÇÃO

**Limpeza Aprovada:** ✅ SIM

**Justificativa:**
- Remove apenas arquivos não-essenciais
- Preserva todo código e documentação
- Melhora organização e profissionalismo
- Totalmente reversível via git

**Próximo Passo:** Executar `prepare_public_repo.sh` e revisar mudanças

---

**Log criado por:** Agente de Auditoria e Preparação de Repositório  
**Data:** 28 de Novembro de 2025  
**Status:** DRAFT (a ser executado)

---

*Este documento será atualizado após execução do script de limpeza.*
