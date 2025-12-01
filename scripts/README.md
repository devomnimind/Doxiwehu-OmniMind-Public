# Scripts Oficiais OmniMind

Repositório de scripts mantidos e testados para operação do sistema OmniMind.

## 🎯 Scripts Canônicos (Oficiais)

Scripts principais que definem e confirmam nossa pesquisa e projeto OmniMind.

### Instalação
- **`canonical/install/install_omnimind.sh`** - Instalação completa do OmniMind
- **`canonical/install/install_systemd_services.sh`** - Instala serviços systemd
- **`canonical/install/setup_security_privileges.sh`** - Configura privilégios de segurança

### Sistema
- **`canonical/system/start_omnimind_system.sh`** ⭐ PRINCIPAL - Sistema completo OmniMind
- **`canonical/system/run_cluster.sh`** - Backend em cluster (portas 8000, 8080, 3001)
- **`canonical/system/start_mcp_servers.sh`** - Inicia servidores MCP
- **`canonical/system/run_mcp_orchestrator.py`** - Orquestrador MCP

### Monitoramento
- **`canonical/monitor/monitor_tests.sh`** - Status pontual de testes
- **`canonical/monitor/monitor_tests_live.sh`** - Monitoramento em tempo real
- **`canonical/monitor/security_monitor.sh`** - Monitoramento de segurança

### Testes
- **`canonical/test/run_tests_by_category.sh`** - Testes por categoria (unit, integration, e2e, quantum, performance)
- **`canonical/test/run_full_certification.sh`** - Certificação completa com GPU/Quantum
- **`canonical/test/run_tests_background.sh`** - Testes em background
- **`canonical/test/run_all_tests_hybrid.py`** - Suite completa de testes híbridos
- **`canonical/test/run_tests.py`** - Executor principal de testes

### Validação
- **`canonical/validate/run_real_metrics.sh`** - Métricas reais com GPU/Quantum
- **`canonical/validate/verify_gpu_setup.sh`** - Verificação de setup GPU
- **`canonical/validate/validate_system.py`** - Validação do sistema
- **`canonical/validate/validate_security.py`** - Validação de segurança
- **`canonical/validate/validate_code.sh`** - Validação de código
- **`canonical/validate/validate_services.sh`** - Validação de serviços

### Diagnóstico
- **`canonical/diagnose/diagnostic_quick.sh`** - Diagnóstico rápido
- **`canonical/diagnose/final_status.sh`** - Status final do sistema
- **`canonical/diagnose/diagnose.py`** - Diagnóstico geral
- **`canonical/diagnose/diagnose_audit.py`** - Diagnóstico de auditoria

## 🛠️ Scripts de Desenvolvimento

Scripts para desenvolvimento, debugging e experimentação.

### Backend
- **`development/backend/run_test_server.py`** - Servidor de teste
- **`development/backend/run_development_observer.py`** - Observer de desenvolvimento
- **`development/backend/start_development_observer.sh`** - Inicia observer

### Frontend
- **`development/frontend/demo_embeddings.py`** - Demo de embeddings
- **`development/frontend/neural_cache_demo.py`** - Demo de cache neural
- **`development/frontend/setup_code_embeddings.py`** - Setup de embeddings
- **`development/frontend/deploy_huggingface.py`** - Deploy para HuggingFace

### Testes
- **`development/test/test_auth.sh`** - Teste de autenticação
- **`development/test/test_*.py`** - Scripts de teste específicos

### Debug
- **`development/debug/debug_imports.py`** - Debug de imports
- **`development/debug/check_*.py`** - Scripts de verificação

## 🔬 Scripts de Pesquisa

Scripts específicos para pesquisa em quantum computing, ML e benchmarks.

### Quantum
- **`research/quantum/demo_ibm_quantum.py`** - Demo IBM Quantum
- **`research/quantum/quantum_benchmark_suite_ibm.py`** - Suite de benchmarks
- **`research/quantum/validate_quantum_*.py`** - Validações quantum

### ML
- **`research/ml/create_training_plan.py`** - Plano de treinamento
- **`research/ml/hybrid_ml_optimizer.py`** - Otimizador híbrido
- **`research/ml/setup_ml_environment.sh`** - Setup ambiente ML

### Benchmarks
- **`research/benchmarks/comprehensive_validation.py`** - Validação abrangente
- **`research/benchmarks/ibm_quantum_real_benchmark.py`** - Benchmark real IBM
- **`research/benchmarks/system_info.py`** - Informações do sistema

## 🛡️ Scripts de Produção

Scripts para deployment, monitoramento e segurança em produção.

### Deploy
- **`production/deploy/install_all_services.sh`** - Instala todos os serviços
- **`production/deploy/fix_systemd_services.sh`** - Corrige serviços systemd
- **`production/deploy/omnimind.service`** - Arquivos de serviço systemd

### Monitoramento
- **`production/monitoring/start_dashboard.sh`** - Inicia dashboard

### Segurança
- **`production/security/setup_production.sh`** - Setup de produção

### Backup
- **`production/backup/automated_backup.sh`** - Backup automatizado

## 🔧 Utilitários

Scripts de manutenção, análise e suporte.

### Manutenção
- **`utilities/maintenance/fix_*.py`** - Scripts de correção
- **`utilities/maintenance/migrate_*.py`** - Scripts de migração
- **`utilities/maintenance/archive_old_docs.sh`** - Arquiva documentação antiga

### Análise
- **`utilities/analysis/analyze_*.py`** - Scripts de análise
- **`utilities/analysis/collect_*.py`** - Scripts de coleta de dados
- **`utilities/analysis/comparative_metrics.py`** - Métricas comparativas

## 📁 Estrutura Final

```
scripts/
├── README.md (este arquivo)
├── canonical/ ⭐ SCRIPTS OFICIAIS
│   ├── install/ - Instalação
│   ├── system/ - Sistema principal
│   ├── monitor/ - Monitoramento
│   ├── test/ - Testes
│   ├── validate/ - Validação
│   └── diagnose/ - Diagnóstico
├── development/ - Desenvolvimento/debug
│   ├── backend/
│   ├── frontend/
│   ├── test/
│   └── debug/
├── research/ - Pesquisa específica
│   ├── quantum/
│   ├── ml/
│   └── benchmarks/
├── production/ - Produção/deploy
│   ├── deploy/
│   ├── monitoring/
│   ├── security/
│   └── backup/
├── utilities/ - Utilitários
│   ├── maintenance/
│   └── analysis/
└── .archive/deprecated/ - Scripts arquivados
```

## ⚠️ Scripts Deprecated

Scripts antigos e não utilizados foram arquivados em `.archive/deprecated/`:
- Scripts duplicados
- Scripts experimentais não funcionais
- Scripts de versões antigas
- Scripts não mantidos

## 🚀 Uso Rápido

```bash
# Sistema completo (PRINCIPAL)
./scripts/canonical/system/start_omnimind_system.sh

# Apenas backend em cluster
./scripts/canonical/system/run_cluster.sh

# Monitorar testes
./scripts/canonical/monitor/monitor_tests_live.sh

# Testes por categoria
./scripts/canonical/test/run_tests_by_category.sh unit

# Validação completa
./scripts/canonical/test/run_full_certification.sh

# Diagnóstico rápido
./scripts/canonical/diagnose/diagnostic_quick.sh
```

## 📝 Notas

- **Scripts Canônicos**: São os scripts oficiais que confirmam nossa pesquisa
- **Caminhos preservados**: Todos os caminhos foram mantidos funcionais
- **Modo desenvolvimento**: Execute `export OMNIMIND_DEV_MODE=false` para validações completas
- **Logs**: Disponíveis em `logs/`, `data/test_reports/`
- **Backup**: Scripts organizados mas não removidos - sempre há backup

