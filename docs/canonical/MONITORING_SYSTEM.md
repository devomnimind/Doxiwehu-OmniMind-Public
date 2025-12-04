
# 🎯 SISTEMA DE MONITORAMENTO PROGRESSIVO & ALERTAS DO OMNIMIND

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Componentes](#componentes)
3. [Como Usar](#como-usar)
4. [Endpoints da API](#endpoints-da-api)
5. [Exemplos Práticos](#exemplos-práticos)
6. [Configuração](#configuração)

---

## 🎯 Visão Geral

O sistema é composto por **3 camadas inteligentes**:

```
┌─────────────────────────────────────────────────┐
│  ALERTAS EM TEMPO REAL (VS Code + WebSocket)   │
│  - Notificações de erros críticos               │
│  - Permissões negadas, servidor caído, etc      │
└─────────────────────────────────────────────────┘
                        ▲
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼────────┐ ┌───▼────────┐ ┌───▼──────────┐
│ Progressive    │ │  Resource  │ │    Alert     │
│ Monitor        │ │ Protector  │ │    System    │
│ - Modo adaptado│ │ - CPU/RAM/ │ │ - Broadcast  │
│ - Snapshots    │ │   Disco    │ │ - Histórico  │
│ - Throttle     │ │ - Matador  │ │ - Rate limit │
│   de relatórios│ │   de procs │ │              │
└────────────────┘ └────────────┘ └──────────────┘
```

---

## 🔧 Componentes

### 1. **ProgressiveMonitor**
Monitora máquina com inteligência adaptativa:

```python
monitor.level = MonitorLevel.IDLE        # 30s entre checks, relatórios a cada 5min
monitor.level = MonitorLevel.NORMAL      # 5s entre checks, relatórios a cada 1min
monitor.level = MonitorLevel.INTENSIVE   # 1s entre checks, relatórios a cada 10s
monitor.level = MonitorLevel.CRITICAL    # 500ms entre checks, relatórios a cada 2s
```

**Características:**
- ✅ Histórico de 1000 snapshots (CPU, RAM, Disco, conexões)
- ✅ Alertas automáticos quando thresholds ultrapassados
- ✅ Relatórios throttled (não inunda com dados)
- ✅ Compressão de histórico (mantém apenas últimas 1000 amostras)

### 2. **ResourceProtector**
Evita que máquina fique travada/sem memória:

```python
protector.mode = "dev"   # 75% CPU, 80% RAM máximo (deixa IDE responsiva)
protector.mode = "test"  # 85% CPU, 85% RAM máximo (mais agressivo)
protector.mode = "prod"  # 90% CPU, 90% RAM máximo (máximo)
```

**O que faz:**
- 🔴 Detecta CPU/RAM/Disco críticos
- 🧹 Limpa caches automaticamente
- ⚡ Reduz prioridade de processos pesados
- 🔪 Mata processos que monopolizam recursos (exceto processos protegidos)

### 3. **AlertSystem**
Distribuição de alertas em tempo real:

```python
AlertType.PERMISSION_ERROR      # Erro ao acessar arquivo
AlertType.SERVER_DOWN           # Backend offline
AlertType.RESOURCE_CRITICAL     # CPU/RAM/Disco crítico
AlertType.TEST_TIMEOUT          # Teste com timeout
```

**Canais:**
- 📡 **WEBSOCKET**: Enviado para frontend em tempo real
- 📡 **VSCODE**: Enviado para extensão do VS Code
- 💾 **FILE**: Salvo em JSON para auditoria
- 📋 **SYSLOG**: Logs estruturados

---

## 💻 Como Usar

### No Backend (main.py)

O sistema já está integrado na lifespan:

```python
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # Já inicializado automaticamente!
    progressive_monitor = app_instance.state.progressive_monitor
    resource_protector = app_instance.state.resource_protector
    alert_system = app_instance.state.alert_system
```

### Em Tarefas Assíncronas

```python
from src.monitor import (
    get_progressive_monitor,
    get_resource_protector,
    get_alert_system,
    MonitorLevel,
)

async def my_background_task():
    monitor = await get_progressive_monitor()
    alerts = await get_alert_system()

    # Aumentar nível de monitoramento se necessário
    if some_condition:
        monitor.set_level(MonitorLevel.INTENSIVE)

    # Emitir alerta customizado
    await alerts.emit(
        alert_type=AlertType.INFO,
        severity="warning",
        title="Tarefa Iniciada",
        message="Processamento de dados iniciado",
        context={"duration_ms": 5000},
        channels={AlertChannel.VSCODE}  # Só para VS Code
    )
```

### Em Plugins de Teste

```python
from src.monitor import get_alert_system

@pytest.fixture(autouse=True)
async def emit_test_alert():
    alerts = await get_alert_system()

    try:
        # Teste executa
        yield
    except TimeoutError as e:
        # Alertar VS Code se timeout
        await alerts.emit_test_timeout(
            test_name=request.node.name,
            timeout_seconds=120,
        )
```

---

## 📡 Endpoints da API

### Health Check
```bash
curl http://localhost:8000/api/monitoring/health
```

**Resposta:**
```json
{
  "cpu": {
    "current": 45.2,
    "limit": 85.0,
    "status": "✅ OK"
  },
  "memory": {
    "current": 62.5,
    "limit": 85.0,
    "available_mb": 3584,
    "status": "✅ OK"
  },
  "disk": {
    "current": 72.1,
    "limit": 90.0,
    "free_gb": 125.4,
    "status": "✅ OK"
  }
}
```

### Alertas Ativos
```bash
curl http://localhost:8000/api/monitoring/alerts/active
```

**Resposta:**
```json
{
  "critical": [
    {
      "id": "1701514800_permission_error",
      "type": "permission_error",
      "severity": "error",
      "title": "Erro de Permissão",
      "message": "Permissão negada em write de /var/log/app.log",
      "timestamp": 1701514800,
      "context": {
        "path": "/var/log/app.log",
        "operation": "write"
      }
    }
  ],
  "recent": [...],
  "total": 5
}
```

### Status Completo
```bash
curl http://localhost:8000/api/monitoring/status
```

### Snapshots Recentes
```bash
curl http://localhost:8000/api/monitoring/snapshots/recent?minutes=10
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Emitir Erro de Permissão

```python
from src.monitor import get_alert_system

async def write_to_log_file(filepath: str, content: str):
    try:
        with open(filepath, "w") as f:
            f.write(content)
    except PermissionError:
        alerts = await get_alert_system()
        await alerts.emit_permission_error(
            path=filepath,
            operation="write",
            context={
                "user": os.getuid(),
                "required_perms": "0644"
            }
        )
        raise
```

### Exemplo 2: Detectar Servidor Caído

```python
from src.monitor import get_alert_system

async def health_check():
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        response.raise_for_status()
    except Exception as e:
        alerts = await get_alert_system()
        await alerts.emit_server_down(
            reason=str(e),
            context={
                "url": "http://localhost:8000/health",
                "timeout": 2,
                "error_type": type(e).__name__
            }
        )
```

### Exemplo 3: Custom Alert com Throttle

```python
from src.monitor import get_alert_system, AlertType, AlertChannel

async def process_heavy_task():
    alerts = await get_alert_system()

    # Emitir alert para VS Code + WebSocket
    # (será throttled: máximo 1 vez por minuto)
    await alerts.emit(
        alert_type=AlertType.INFO,
        severity="warning",
        title="Processamento Pesado",
        message="Tarefa usando 80% de CPU",
        context={
            "cpu_percent": 80,
            "estimated_duration": "5min"
        },
        channels={
            AlertChannel.VSCODE,
            AlertChannel.WEBSOCKET
        }
    )
```

### Exemplo 4: Ajustar Nível de Monitoramento

```python
from src.monitor import get_progressive_monitor, MonitorLevel

async def start_intensive_testing():
    monitor = await get_progressive_monitor()

    # Aumentar monitoramento durante testes
    monitor.set_level(MonitorLevel.INTENSIVE)

    try:
        # Executar testes
        await run_test_suite()
    finally:
        # Voltar ao normal depois
        monitor.set_level(MonitorLevel.NORMAL)
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# Modo de execução (dev/test/prod)
OMNIMIND_MODE=test

# Diretório de dados dos alertas
OMNIMIND_MONITOR_DATA_DIR=data/monitor

# Alertas (opcional)
OMNIMIND_DISABLE_ALERTS=False
```

### Thresholds Padrão

```python
# Em ProgressiveMonitor.__init__
self.thresholds = {
    "cpu_warning": 70.0,      # CPU >70% = warning
    "cpu_critical": 85.0,     # CPU >85% = critical
    "memory_warning": 75.0,   # RAM >75% = warning
    "memory_critical": 90.0,  # RAM >90% = critical
    "disk_warning": 80.0,     # Disco >80% = warning
    "disk_critical": 95.0,    # Disco >95% = critical
}
```

Para customizar, edite `src/monitor/progressive_monitor.py` antes de iniciar.

## 📘 Referências Técnicas (Conciliação)

- A [documentação do módulo](src/monitor/README.md) alinha o conteúdo oficial de cada componente descrito aqui.
- O [ProgressiveMonitor](src/monitor/progressive_monitor.py) controla níveis (`MonitorLevel`), thresholds e relatórios throttled que aparecem na seção de Componentes.
- O [ResourceProtector](src/monitor/resource_protector.py) aplica limites por modo dev/test/prod e executa os handlers de CPU/RAM/Disco mencionados na seção de ResourceProtector.
- O [AlertSystem](src/monitor/alert_system.py) responde pelos tipos de alertas, persistência JSON e handlers de canais (WebSocket/VS Code/Syslog/File) descritos na seção de Alertas.
- As rotas reais vivem em [web/backend/routes/monitoring.py](web/backend/routes/monitoring.py), que expõe `/api/monitoring/health`, `/alerts/active`, `/status` e `/snapshots/recent` usados nos exemplos deste documento.
- O [lifespan do backend](web/backend/main.py#L220-L322) inicializa ProgressiveMonitor, ResourceProtector e AlertSystem e registra os handlers de broadcast via WebSocket.
- Scripts utilitários como [scripts/view_monitoring_alerts.py](scripts/view_monitoring_alerts.py) consomem as mesmas rotas e ajudam a validar os valores exibidos aqui.

---

## 🔗 Integração com VS Code

O VS Code pode receber alertas via WebSocket:

1. **Status Bar**: Mostra status atual (CPU/RAM/Disco)
2. **Notifications**: Pop-ups para alertas críticos
3. **Output Channel**: Log estruturado de todos os eventos

Exemplo de conexão VS Code:

```typescript
const ws = new WebSocket(
  "ws://localhost:8000/ws?auth_token=" + getAuthToken()
);

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  if (msg.type === "alert") {
    // Mostrar notificação no VS Code
    vscode.window.showErrorMessage(
      `[${msg.severity.toUpperCase()}] ${msg.title}: ${msg.message}`
    );

    // Atualizar status bar
    statusBar.text = `CPU: ${msg.context.cpu_percent}%`;
  }
};
```

---

## 📊 Histórico de Alertas

Todos os alertas são salvos em JSON:

```
data/alerts/
├── alert_1701514800_permission_error.json
├── alert_1701514801_server_down.json
├── alert_1701514802_resource_critical.json
└── alerts_index.json  # Índice dos últimos 500 alertas
```

**Query para ver alertas críticos:**

```bash
cat data/alerts/alerts_index.json | jq '.[] | select(.severity=="critical")'
```

---

## 🎯 Próximas Melhorias

- [ ] Webhooks customizados (Slack, Discord, etc)
- [ ] Machine learning para predicção de crashes
- [ ] Métricas agregadas por hora/dia
- [ ] Dashboard real-time de recursos
- [ ] Integração com Prometheus/Grafana

---

**Desenvolvido com ❤️ para OmniMind**
