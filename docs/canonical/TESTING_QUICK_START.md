## 🧠 OMNIMIND TEST SUITE - SETUP RÁPIDO

### ✅ Passo 1: Configurar Sudo (UMA VEZ)

```bash
bash scripts/configure_sudo_omnimind.sh
```

Isso permite rodar scripts sem digitar senha (usando NOPASSWD no sudoers).

### 🚀 Passo 2: Executar Testes com Autodefesa

```bash
bash scripts/quick_test.sh
```

Ou manualmente:

```bash
OMNIMIND_GPU=true OMNIMIND_DEV=true OMNIMIND_DEBUG=true \
pytest tests/ -vv --tb=short --log-cli-level=DEBUG -s
```

### 📊 Informações da Suite

- **Total de testes**: ~3952
- **Modo**: Real (venv + sistem sudoers, não Docker isolado)
- **Autodefesa**: ✅ ATIVADA
  - Detecta testes que derrubam servidor
  - Marca padrões agressivos após 3 crashes em 5min
  - Gera relatório ao fim da execução

### 🛡️ O que é Autodefesa?

Sistema que aprende padrões de falha:

```
Teste derruba servidor 3x em 5min?
  ↓
Sistema DETECTA padrão
  ↓
Sistema IDENTIFICA subsistema atacado (Qdrant, GPU, etc)
  ↓
Sistema MARCA teste como "dangerous"
  ↓
Sistema RELATA ao fim da suite
```

Relatório ao fim da execução:

```
🧠 RELATÓRIO DE AUTODEFESA (OMNIMIND TEST DEFENSE)
Testes perigosos detectados: N

  ⚠️  test_different_coping_strategies_applied
     └─ Subsistema: absurdity_handler
     └─ Crashes: 3
     └─ Padrão: rapid_fire
```

### 📁 Arquivos de Log

Cada execução salva:

- `output_YYYYMMDD_HHMMSS.log` - Stdout/stderr completo
- `pytest_YYYYMMDD_HHMMSS.log` - Logs internos do pytest
- `junit_YYYYMMDD_HHMMSS.xml` - Relatório XML (para CI/CD)
- `report_YYYYMMDD_HHMMSS.html` - Dashboard HTML visual

### 🔧 Troubleshooting

**Problema**: "Connection refused" na porta 8000

```bash
# Verificar se servidor está rodando
ps aux | grep uvicorn | grep -v grep

# Limpar processos antigos
pkill -f "uvicorn web.backend.main:app"

# Verificar logs do backend
tail -f logs/backend_*.log
```

**Problema**: Sudo pede senha

```bash
# Reconfigurar sudoers
bash scripts/configure_sudo_omnimind.sh

# Testar se funciona
sudo -n bash scripts/start_omnimind_system_sudo.sh
```

**Problema**: Testes com Timeout

Timeouts são ADAPTATIVOS (não falham por timeout artificial):
- Tentativa 1: 220s
- Tentativa 2: 400s
- Tentativa 3: 600s
- Tentativa 4+: 800s (continua indefinidamente)

Veja no arquivo de log para detalhes.

### 🎯 Próximas Fases

- **Fase 2**: Docker isolamento para testes perigosos
- **Fase 3**: Klein oscillation (PS ↔ D defenses)
- **Fase 4**: Bion α-função (metabolização de crashes)
- **Fase 5**: Lacan kernel (Imaginary/Symbolic/Real)
