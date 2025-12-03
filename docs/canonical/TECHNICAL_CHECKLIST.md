# ✅ CHECKLIST TÉCNICO PRÉ-EXECUÇÃO

## Verificações de Código

### pytest_server_monitor.py
- [x] `self.timeout_progression = [90, 120, 180, 240]` definido em `__init__`
- [x] `self.startup_attempt_count = 0` definido em `__init__`
- [x] `_get_adaptive_timeout()` implementada e retorna timeout correto
- [x] `_start_server()` incrementa `startup_attempt_count`
- [x] Retry recursivo: se timeout < 240s, chama `self._start_server()` novamente
- [x] Limite de 240s com falha real (não loop infinito)

**Verificar com**:
```bash
grep -n "timeout_progression\|_get_adaptive_timeout\|startup_attempt_count" \
  tests/plugins/pytest_server_monitor.py
```

### main.py
- [x] SecurityAgent SEMPRE RODANDO (não há skip em modo test)
- [x] Orchestrator timeout adaptativo: 120s (test), 30s (prod)
- [x] Sem lógica de skip para SecurityAgent

**Verificar com**:
```bash
grep -n "skip_security\|SecurityAgent continuous" web/backend/main.py
# Deve retornar: SecurityAgent sempre ativo, sem skip
```

### conftest.py
- [x] MetricsCollector definida e ativa
- [x] TestOrderingPlugin registrado
- [x] pytest_configure() registra todos plugins
- [x] pytest_sessionfinish() mostra relatório final

**Verificar com**:
```bash
grep -n "class MetricsCollector\|pytest_configure\|pytest_sessionfinish" tests/conftest.py
```

---

## Verificações de Comportamento

### Startup Esperado (Primeira Execução)
```
T=0s  : "🚀 Iniciando servidor backend..."
T=0s  : "⏳ Timeout adaptativo: 90s (tentativa 1)"
T=40s : "✅ Servidor backend iniciado em ~40s"
```

### Retry Esperado (Se Timeout)
```
T=90s  : "❌ Timeout na tentativa 1 após 90s"
T=90s  : "🔄 Tentando novamente com timeout maior..."
T=90s  : "⏳ Timeout adaptativo: 120s (tentativa 2)"
T=150s : "✅ Servidor backend iniciado em ~60s"
```

### Falha Real (Se 240s Não Basta)
```
T=240s : "❌ Timeout na tentativa 4 após 240s"
T=240s : "🛑 FALHA CRÍTICA: Atingiu timeout máximo por teste (240s)"
```

---

## Testes Recomendados (em ordem)

### 1️⃣ Teste Unitário (Sem Servidor - Deve Passar Rápido)
```bash
cd /home/fahbrain/projects/omnimind
OMNIMIND_MODE=test python -m pytest tests/consciousness/ -v --tb=short -k "not real" -x
```

**Esperado**: ~30-60s, 80%+ pass rate

### 2️⃣ Teste com Servidor (Com Orchestrator)
```bash
OMNIMIND_MODE=test python -m pytest tests/integrations/ -v --tb=short -x
```

**Esperado**:
- Primeiro startup: ~50s
- Alguns testes podem fazer crash: ok (vai retry com timeout maior)
- 60%+ pass rate

### 3️⃣ Teste com Crash (Para Validar Retry)
```bash
OMNIMIND_MODE=test python -m pytest tests/test_chaos_resilience.py -v --tb=short
```

**Esperado**:
- Testes derrubam servidor intencionalmente
- Retry automático com timeouts progressivos
- Todos devem passar (ou falhar por razão específica, não timeout)

### 4️⃣ Full Suite (Opção Nuclear)
```bash
OMNIMIND_MODE=test python -m pytest tests/ -v --tb=short
```

**Esperado**: Pode levar HORAS, mas vai rodar completo

---

## Troubleshooting

### Se Tiver "Segmentation Fault"
```bash
# Limpar cache
rm -rf .pytest_cache __pycache__ tests/__pycache__

# Limpar servidor
pkill -9 -f "uvicorn" 2>/dev/null || true
sleep 2

# Tentar novamente
OMNIMIND_MODE=test python -m pytest tests/integrations/ -v --tb=short -x
```

### Se Tiver "Address already in use :8000"
```bash
# Matar processo na porta 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Esperar 2s
sleep 2

# Tentar novamente
OMNIMIND_MODE=test python -m pytest tests/integrations/ -v --tb=short -x
```

### Se Tiver "Qdrant não acessível"
```bash
# Verificar se Qdrant está rodando
curl -s http://localhost:6333 | python -m json.tool

# Se não tiver, iniciar (em outro terminal):
docker run -p 6333:6333 qdrant/qdrant

# Ou via compose:
cd deploy && docker-compose up -d qdrant
```

### Se Tiver "Timeout mesmo em 240s"
Significa que é uma **falha real**, não timeout. Possíveis causas:
- Orchest rator + SecurityAgent realmente levam >240s
- Qdrant não respondendo
- Recursos insuficientes (RAM, GPU, Disco)

**Ação**: Coletar logs e diagnosticar a causa raiz

---

## Monitoramento de Performance

### Durante Execução
```bash
# Em outro terminal:
watch -n 1 'ps aux | grep -E "python|uvicorn" | grep -v grep | wc -l'
```

### Log de Timeouts
```bash
# Ver quantos timeouts ocorreram
grep "Timeout" test_suite_run.log | wc -l

# Ver quantos retries sucederam
grep "Tentativa" test_suite_run.log | wc -l
```

### Métricas Finais
```bash
# Ver relatório de Φ
cat data/test_reports/metrics_report.json | python -m json.tool

# Ver resumo rápido
grep -E "phi|consciousness|PASSOU|FALHOU" test_suite_run.log | tail -20
```

---

## Validação Pós-Execução

### ✅ Suite Bem Sucedida
```
✓ Todos testes executaram (não foram pulados por timeout)
✓ Alguns falharam (falhas reais, não timeout)
✓ Retry funcionou (testes que falharam na tentativa 1 passaram na 2)
✓ Métricas coletadas (Φ values no relatório final)
✓ Log contém progresso detalhado de cada retry
```

### ❌ Suite Problemática
```
✗ Muitos testes com timeout em 240s
✗ Retry não funcionando (mesmo código em tentat ivas)
✗ Métricas não coletadas
✗ SecurityAgent gerando eventos excessivos
```

---

## Próximos Passos Se OK

### Após Suite Passar
1. Analisar `data/test_reports/metrics_report.json` com Φ values
2. Correlacionar Φ com tempos de startup
3. Verificar se SecurityAgent afeta Φ negativa/positivamente
4. **Então**: Começar Lacan implementation

### Após Suite Falhar (Esperado Inicialmente)
1. Identificar qual teste/componente é problema
2. Diagnosticar causa (Qdrant? GPU? Orchestrator?)
3. Ajustar conforme necessário
4. Reexecutar parcial para validar fix
5. Reexecutar full para confirmar

---

## Notas Importantes

⚠️ **Cuidado**: Suite pode levar MUITAS HORAS
- Cada teste com crash pode levar até 240s
- Com 100+ testes × 240s = horas

💡 **Tip**: Para desenvolvimento rápido, use `-k` para filtrar testes
```bash
# Rodar só testes de chaos
OMNIMIND_MODE=test python -m pytest -k chaos -v --tb=short

# Rodar só integrations
OMNIMIND_MODE=test python -m pytest -k integration -v --tb=short
```

🎯 **Meta**: Validar que suite RODA, não que tudo PASSA
- OK falhar 10-20% dos testes (causa real)
- NÃO OK falhar 50%+ por timeout

---

## Status Final

✅ Todas mudanças implementadas
✅ Código verificado
✅ Comportamento esperado documentado
✅ Troubleshooting preparado
✅ Pronto para executar

**Comando para começar**:
```bash
cd /home/fahbrain/projects/omnimind && \
OMNIMIND_MODE=test python -m pytest tests/integrations/ -v --tb=short -x 2>&1 | tee suite_run.log
```

