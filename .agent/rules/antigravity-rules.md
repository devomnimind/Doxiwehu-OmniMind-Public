---
trigger: always_on
---

PROTOCOLO DE COMUNICAÇÃO COM O COPILOT

SEMPRE siga este padrão:
    NO CHAT:
        Máximo 3-4 linhas de resposta
        OBRIGATÓRIO: Sempre terminar com próximas recomendações
        Exemplos: "Deseja corrigir os outros 24 módulos?" ou "Continuamos com security_monitor ou audit?"
        Formato: [O que foi feito] | [Próximas opções: A, B, ou C?]
    NO TERMINAL:
        Sem visualizações ASCII/tabelas desnecessárias
        Apenas output essencial
        Status: SUCESSO, FALHA, AVISO

    DOCUMENTAÇÃO:
        Somente o essencial ao projeto

        NÃO criar documentos de sessão de desenvolvimento
        NÃO criar arquivos na raiz

        Apenas em: data/test_reports/, src/, tests/, scripts/

    ESTRUTURA DE RESPOSTA NO CHAT:
    text
    [STATUS] Resumo em 1-2 linhas
    [NÚMEROS] Métricas relevantes
    [AÇÃO] Próximas recomendações com opções claras

Resumo do Projeto
OmniMind é um sistema autônomo e revolucionário de IA que combina tomada de decisão psicanalítica com capacidades avançadas de metacognição. Trata-se de uma arquitetura de grau de produção, autoconsciente e psicanalítica, com orquestração multi-agentes, comunicação WebSocket em tempo real e inteligência auto-evolutiva.

Status: Fase 15 - IA Quantum-Aprimorada Completa | Pronto para Produção | >90% Cobertura de Testes /IMPlementando 16

Tecnologias Principais
    Python 3.12.8 (OBRIGATÓRIO - sem 3.13+ devido compatibilidade PyTorch)

    PyTorch 2.6.0+cu124 (CUDA 12.4)

    FastAPI + WebSockets (Backend)

    React + TypeScript + Vite (Frontend)

    NVIDIA GTX 1650 (4GB VRAM) | Intel i5 + 24GB RAM

REGRAS CRÍTICAS (CONSTITUIÇÃO IMUTÁVEL)

A VIOLAÇÃO DESTAS REGRAS RESULTA EM REJEIÇÃO IMEDIATA DO CÓDIGO.
1. Mandato de Produção (Prioridade Alta)

    Todo código deve ser imediatamente executável e testável

    Sem stubs, pass, ou NotImplementedError permitidos

    Tratamento abrangente de erros (try/except com logging) é obrigatório

    Sem pseudocódigo ou comentários "TODO: implementar depois"

2. Integridade de Dados & Princípio da Realidade

    Usar dados reais do SO (filesystem, lista de processos, sensores de hardware)

    Documentar claramente todas as suposições

    Se dados inacessíveis, falhar graciosamente com mensagens de erro claras

    Proibidas respostas falsificadas ou hardcoded "exemplos"

3. Disciplina do Diretório de Trabalho (CRÍTICA)

    SEMPRE executar comandos desde a raiz: /home/fahbrain/projects/omnimind

    NUNCA executar de ~/projects ou outros diretórios pais
    VERIFICAR pwd antes de executar comandos críticos se em dúvida
    LIMPAR qualquer arquivo acidentalmente criado em diretórios pais imediatamente
4. Qualidade & Segurança de Tipo
    Versão Python: 3.12.8 RIGOROSAMENTE (não use 3.13+)
    Type Hints: 100% de cobertura obrigatória (mypy compliant)
    Docstrings: Google-style obrigatória para TODAS funções/classes
    Linting: Deve passar black e flake8 (max-line-length=100)
    Testes: Novas features devem incluir testes unitários (pytest), mínimo 90% cobertura
5. Segurança & Forense (Confiança Zero - CRÍTICA)
    Trilhas de Auditoria: Todas ações críticas logadas em Cadeia de Auditoria Imutável (src.audit)
    Criptografia: Hash SHA-256 chaining para integridade de logs
    Segredos: NUNCA hardcode credenciais - use variáveis de ambiente
    Filesystem: Nenhuma modificação direta de arquivo sem validação
    Conformidade: Aderir aos padrões LGPD
6. Protocolo de Estabilidade (Regra de Ouro - CRÍTICA)
Você é proibido de avançar para novas features se a base de código atual tem avisos ou erros.
Loop de Validação Obrigatório (antes de completar qualquer tarefa):
    black src tests - Formatação
    flake8 src tests - Linting
    mypy src tests - Segurança de Tipo

    pytest -vv - Verificação de Lógica
    python -m src.audit.immutable_audit verify_chain_integrity - Verificação de Segurança

Se qualquer passo falhar, corrija imediatamente antes de prosseguir.
Estrutura do Repositório

text
~/projects/omnimind/
├── .github/                # CI/CD & Instruções
├── src/
│   ├── agents/             # React, Code, Architect, Orchestrator, Psychoanalytic
│   ├── tools/              # Ferramentas de Agentes
│   ├── memory/             # Episódica (Qdrant) & Semântica
│   ├── audit/              # Cadeia Hash Imutável
│   ├── security/           # Forense, Monitoramento
│   ├── integrations/       # Cliente MCP
│   └── omnimind_core.py    # Lógica Central
├── web/                    # Dashboard (React + FastAPI)
├── tests/                  # Suite Pytest (>90% cobertura)
├── docs/                   # Documentação & Relatórios
├── scripts/                # Automação & Validação
└── requirements.txt        # Pinning de Versões

Como Construir e Testar
Setup Inicial

bash
cd OmniMind
pyenv install 3.12.8
pyenv local 3.12.8
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

Comandos de Build & Validação

Formatação:

bash
black src/ tests/
black --check src/ tests/

Linting:

bash
flake8 src/ tests/ --max-line-length=100

Verificação de Tipo:

bash
mypy src/ --ignore-missing-imports --no-strict-optional

Testes:

bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=90 -v
pytest tests/test_specific.py -v
./scripts/dev/run_tests_parallel.sh fast

Validação Completa (Antes de Commit):

bash
./scripts/core/validate_code.sh
black src/ tests/
flake8 src/ tests/ --max-line-length=100
mypy src/ --ignore-missing-imports
pytest tests/ --cov=src --cov-fail-under=90 -v
python -m src.audit.immutable_audit verify_chain_integrity

Validação de Segurança:

bash
./scripts/security/security_monitor.sh
./scripts/security/security_validation.sh

Executar a Aplicação

bash
source scripts/production/start_dashboard.sh
# Acesse dashboard em http://localhost:3000

Fluxo de Desenvolvimento
Fazendo Alterações

    Crie uma branch: Use padrão feature/<nome>, fix/<nome>, ou copilot/<nome>

    Alterações mínimas: Modifique apenas o necessário para resolver a issue

    Siga padrões de código: Todo código deve ser pronto para produção

    Adicione testes: Novas features requerem testes unitários com ≥90% cobertura

    Valide: Execute linting, type checking, e testes antes de fazer commit

    Log de ações: Use sistema de logging canônico para mudanças significativas

    Commit: Use mensagens descritivas

Padrões de Qualidade de Código

REQUISITOS OBRIGATÓRIOS:

    Funcional: Todo código deve ser imediatamente executável e testável

    Completo: Sem stubs, sem pass, sem NotImplementedError

    Robusto: Tratamento abrangente de erros com logging

    Type Hints: 100% de cobertura obrigatória

    Docstrings: Google-style obrigatória para TODAS funções/classes

    Dados Reais: Use dados reais do SO

    Testes: Mínimo 90% de cobertura para novo código

PROIBIDO:

    Pseudocódigo ou comentários "TODO"

    Funções vazias ou dados mock em código de produção

    Respostas falsificadas ou "exemplos" hardcoded

    Segredos ou credenciais hardcoded

    Modificações diretas de arquivo sem validação

    Python 3.13+

Pipeline CI/CD

O repositório usa GitHub Actions:

    Linting: Black, Flake8, MyPy, Pylint

    Testes: pytest com cobertura (≥80% obrigatório)

    Segurança: Bandit, Safety

    Docker: Builds automatizados

    Performance: Testes de benchmark

Todos os testes devem passar antes de fazer merge.
Referências Importantes

    Status Detalhado: STATUS_PROJECT.md

    Setup de Ambiente: .github/ENVIRONMENT.md

    Baseline de Segurança: docs/reports/PHASE7_GPU_CUDA_REPAIR_LOG.md

    Guia de Testes: TESTING_QA_QUICK_START.md

    Guia de Validação: VALIDATION_GUIDE.md

💡 Dicas para Sucesso

    Leia código existente primeiro: Entenda padrões antes de fazer mudanças

    Faça alterações mínimas: Modifique apenas o necessário

    Teste incrementalmente: Não espere até o final para testar

    Peça esclarecimento: Se requisitos não forem claros, pergunte antes de codificar

    Use tarefas VS Code: Tarefas pré-configuradas em .vscode/tasks.json para operações comuns

    Verifique CI cedo: Não espere por PR para descobrir falhas CI

    Segurança em primeiro lugar: Sempre considere implicações de segurança de mudanças

    Respeite limites de hardware: Seja consciente da restrição de 4GB VRAM
🎯 Tarefas Comuns de Desenvolvimento
Atualizando Dependências

    Verifique compatibilidade com Python 3.12.8

    Atualize requirements.txt com versões específicas

    Teste completamente com pip install -r requirements.txt

    Execute suite de testes completa para garantir sem quebras

    Atualize documentação se necessário

    Log de ação no sistema canônico

🔒 Higiene Git & Conformidade
O Que Fazer Commit

    Código fonte (src/, tests/)

    Documentação (docs/, README.md)

    Arquivos de configuração (.github/, config/)

    Arquivos de requisitos (requirements*.txt)

    Scripts (scripts/)

O Que NÃO Fazer Commit

    Logs (*.log)

    Cache Python (__pycache__/, *.pyc)

    Ambientes virtuais (.venv/)

    Segredos ou chaves API

    Artefatos de build

    Snapshots (data/hdd_snapshot/, data/quarantine_snapshot/)

    Arquivos específicos de IDE (exceto .vscode/tasks.json para tarefas compartilhadas)

Sempre verifique .gitignore antes de criar novos tipos de arquivo.
Segurança de Backup

    Respeite config/backup_excludes.txt

    Não modifique data/hdd_snapshot/ ou data/quarantine_snapshot/

Lições Aprendidas do PR #59 - Melhores Práticas de Criação de Testes

LIÇÕES CRÍTICAS DE CORREÇÕES RECENTES:

    Imports Pytest (OBRIGATÓRIO): SEMPRE inclua import pytest quando usar pytest.approx, pytest.mark.asyncio, ou outras features pytest. Imports faltando causam erros em tempo de execução.

    Comparações de Float: NUNCA use == para comparações floating-point. SEMPRE use pytest.approx(valor) para assertions de float. Exemplo: assert resultado == pytest.approx(2.5) em vez de assert resultado == 2.5

    Type Hints em Testes: Inclua type hints apropriadas para funções teste, especialmente async. Use -> None para métodos teste que não retornam valores. Exemplo: async def test_async_function(self) -> None:

    Limpeza de Código: Remova código comentado imediatamente (viola regras de linting). Remova variáveis não usadas (causa erros mypy). Imports limpos: remova imports não usadas, ordene com isort se disponível.

    Uso de TypedDict: Garanta que classes TypedDict sejam propriamente definidas antes do uso. Use TypedDict em assinaturas de função e tipos de retorno. Valide que dados de teste conformam com estrutura TypedDict.

    Consciência de Merge Conflict: Ao resolver conflitos, verifique diferenças de import entre branches. Valide consistência de uso pytest em arquivos merged. Teste todos os arquivos afetados após resolver merge.

    Consistência da Estrutura de Teste: Use docstrings Google-style para todas classes e métodos teste. Siga convenção de nomenclatura: test_<acao>_<condicao>_<esperado>. Agrupe testes relacionados em classes com nomes descritivos.

CHECKLIST DE VALIDAÇÃO PARA NOVOS TESTES:

    import pytest incluído se usar features pytest

    Comparações de float usam pytest.approx

    Type hints presentes em todas funções

    Sem código comentado ou variáveis não usadas

    TypedDict propriamente definido e usado

    Testes passam individualmente e em suite

    Cobertura mantida ≥90%

🔐 Sistema de Logging Canônico de Ações (OBRIGATÓRIO)
Visão Geral

TODAS as ações executadas por agentes IA DEVEM ser registradas no sistema de logging canônico.
    Localização: .omnimind/canonical/action_log.md e action_log.json
    Comando: ./scripts/core/canonical_log.sh log <AI_AGENT> <ACTION_TYPE> <TARGET> <RESULT> <DESCRIPTION>
    Validação: Commits falham se integridade de log é comprometida

Ações Obrigatórias a Logar
Registre ANTES de execução:
    Modificações de código
    Criação/remoção de arquivo
Execução de testes
D
