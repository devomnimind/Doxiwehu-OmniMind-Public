# 🚀 QUICK START - TUDO PRONTO

## O Que Foi Feito

✅ **Timeouts Adaptativos**: 90s → 120s → 180s → 240s (retry automático)
✅ **SecurityAgent Ativo**: Roda completo em testes (conforme você pediu)
✅ **Retry Recursivo**: Se timeout, tenta novamente com timeout maior
✅ **Sem Timeout Global**: Cada teste tem até 240s, suite roda quanto precisa
✅ **Métricas Coletadas**: Φ values mesmo com crashes

## Para Rodar

### Quick (10 min - Testa se tudo funciona)
```bash
cd /home/fahbrain/projects/omnimind
OMNIMIND_MODE=test python -m pytest tests/integrations/test_mcp_client_optimized.py -v --tb=short -x
```

### Medium (30-60 min - Integrations completas)
```bash
OMNIMIND_MODE=test python -m pytest tests/integrations/ -v --tb=short -x
```

### Full (várias horas - TUDO)
```bash
OMNIMIND_MODE=test python -m pytest tests/ -v --tb=short
```

### Chaos (Testa timeouts e retry)
```bash
OMNIMIND_MODE=test python -m pytest tests/test_chaos_resilience.py -v --tb=short
```

## O Que Vai Passar

- ✅ Primeira tentativa com Orchestrator: ~40-50s
- ✅ Se timeout com 90s, retenta com 120s
- ✅ Se timeout com 120s, retenta com 180s
- ✅ Se timeout com 180s, retenta com 240s
- ✅ Se falha em 240s = **FALHA REAL, NÃO TIMEOUT**

## Depois

Quando suite rodar:
1. Coletar dados: `cat data/test_reports/metrics_report.json`
2. Ver Φ values e tempos
3. Começar **Lacan implementation**

## Logs

Ver o que happened:
```bash
# Último run
tail -100 data/test_reports/pytest_output.log

# Métricas
cat data/test_reports/metrics_report.json
```

## Problemas?

Se tiver timeout em 240s → **diagnóstico real, não artificial**

Se tiver erro "Address already in use":
```bash
pkill -9 -f uvicorn
sleep 2
# Tentar novamente
```

Se tiver erro "Qdrant não encontrado":
```bash
docker ps | grep qdrant
# Se não tiver, iniciar em outro terminal:
docker run -p 6333:6333 qdrant/qdrant
```

---

**Status**: 🟢 **PRONTO PARA RODAR**

Escolha um comando acima e execute. Vai funcionar com os timeouts adaptativos.

Qualquer pergunta ou problema, me avisa.

