# 🏗️ Arquitetura Distribuída e Escalabilidade - OmniMind Evolution
## Documento 2: Sistemas Distribuídos e Real-Time Learning

**Projeto:** OmniMind - Sistema de IA Autônomo  
**Categoria:** Arquitetura Técnica  
**Versão:** 1.0  
**Data:** Novembro 2025  
**Idioma:** Português BR (Comandos e código em English)

---

## 📑 Sumário Executivo

Este documento detalha a arquitetura distribuída do OmniMind e os sistemas de aprendizado em tempo real, cobrindo: (1) Escalabilidade Horizontal com clusterização, (2) Real-Time Learning com online algorithms, e (3) Integração com infraestrutura existente.

---

## 🌐 Parte 1: Escalabilidade Horizontal

### 1.1 Visão Arquitetural

**Transição: Single-Node → Distributed Cluster**

```
┌─────────────────────────────────────────────────────┐
│           CURRENT (Single Node)                      │
│  ┌──────────────────────────────────────┐           │
│  │  OmniMind Instance                   │           │
│  │  - Agents                            │           │
│  │  - Memory (Qdrant)                   │           │
│  │  - LLM Inference                     │           │
│  │  GTX 1650 (4GB VRAM)                │           │
│  └──────────────────────────────────────┘           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│           TARGET (Distributed Cluster)               │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Node 1       │  │ Node 2       │  │ Node 3    │ │
│  │ (Leader)     │  │ (Worker)     │  │ (Worker)  │ │
│  │              │  │              │  │           │ │
│  │ - Orchestr.  │  │ - Inference  │  │ - Memory  │ │
│  │ - Consensus  │  │ - Agents     │  │ - Cache   │ │
│  │ GTX 1650     │  │ GTX 1650     │  │ CPU-only  │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│         │                 │                 │        │
│         └─────── Service Mesh ──────────────┘        │
└─────────────────────────────────────────────────────┘
```

### 1.2 Componentes Principais

#### Service Registry & Discovery

```python
# src/scaling/service_registry.py
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class NodeStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNREACHABLE = "unreachable"

@dataclass
class NodeInfo:
    node_id: str
    ip_address: str
    port: int
    capabilities: List[str]
    status: NodeStatus
    last_heartbeat: datetime
    load_factor: float
    
class ServiceRegistry:
    """Registro centralizado de nós do cluster"""
    
    def __init__(self):
        self.nodes: Dict[str, NodeInfo] = {}
        self.capability_index: Dict[str, List[str]] = {}
        
    async def register_node(
        self,
        node_id: str,
        ip_address: str,
        port: int,
        capabilities: List[str]
    ) -> NodeInfo:
        """Registra novo nó no cluster"""
        
        node = NodeInfo(
            node_id=node_id,
            ip_address=ip_address,
            port=port,
            capabilities=capabilities,
            status=NodeStatus.HEALTHY,
            last_heartbeat=datetime.now(),
            load_factor=0.0
        )
        
        self.nodes[node_id] = node
        
        # Indexa por capabilities
        for capability in capabilities:
            if capability not in self.capability_index:
                self.capability_index[capability] = []
            self.capability_index[capability].append(node_id)
        
        logger.info(f"Node {node_id} registered with {len(capabilities)} capabilities")
        return node
    
    def discover_service(self, capability: str) -> List[NodeInfo]:
        """Descobre nós com capability específica"""
        
        if capability not in self.capability_index:
            return []
        
        node_ids = self.capability_index[capability]
        
        # Filtra apenas nós saudáveis
        healthy_nodes = [
            self.nodes[nid] for nid in node_ids
            if self.nodes[nid].status == NodeStatus.HEALTHY
        ]
        
        return healthy_nodes
```

**Exemplo de uso:**
```python
# Inicializar registry
registry = ServiceRegistry()

# Nó 1: Coordenador + Inference
await registry.register_node(
    node_id="node-1",
    ip_address="192.168.1.10",
    port=8000,
    capabilities=["orchestration", "inference", "consensus"]
)

# Nó 2: Worker especializado em inference
await registry.register_node(
    node_id="node-2",
    ip_address="192.168.1.11",
    port=8000,
    capabilities=["inference", "agents"]
)

# Descobrir nós para inferência
inference_nodes = registry.discover_service("inference")
print(f"Nós disponíveis para inferência: {len(inference_nodes)}")
```

#### Raft Consensus Protocol

```python
# src/scaling/raft_consensus.py
from enum import Enum
import asyncio

class NodeState(Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"

@dataclass
class LogEntry:
    term: int
    index: int
    command: Dict[str, Any]

class RaftNode:
    """Implementação simplificada de Raft"""
    
    def __init__(self, node_id: str, cluster_nodes: List[str]):
        self.node_id = node_id
        self.cluster_nodes = cluster_nodes
        self.state = NodeState.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.log: List[LogEntry] = []
        self.commit_index = 0
        self.last_applied = 0
        
        # Timers
        self.election_timeout = random.uniform(150, 300)  # ms
        self.heartbeat_interval = 50  # ms
        
    async def start(self):
        """Inicia nó Raft"""
        
        if self.state == NodeState.FOLLOWER:
            asyncio.create_task(self._follower_loop())
        elif self.state == NodeState.LEADER:
            asyncio.create_task(self._leader_loop())
    
    async def _follower_loop(self):
        """Loop de follower"""
        
        while self.state == NodeState.FOLLOWER:
            # Aguarda heartbeat do leader
            await asyncio.sleep(self.election_timeout / 1000)
            
            # Se timeout sem heartbeat, inicia eleição
            if self._should_start_election():
                await self._start_election()
    
    async def _start_election(self):
        """Inicia processo de eleição"""
        
        self.state = NodeState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        votes_received = 1
        
        logger.info(f"Node {self.node_id} starting election for term {self.current_term}")
        
        # Solicita votos dos peers
        for peer in self.cluster_nodes:
            if peer != self.node_id:
                vote_granted = await self._request_vote(peer)
                if vote_granted:
                    votes_received += 1
        
        # Maioria simples
        majority = (len(self.cluster_nodes) + 1) // 2
        if votes_received > majority:
            self._become_leader()
        else:
            self.state = NodeState.FOLLOWER
    
    def _become_leader(self):
        """Torna-se líder do cluster"""
        
        self.state = NodeState.LEADER
        logger.info(f"Node {self.node_id} became leader for term {self.current_term}")
        
        # Inicia heartbeat loop
        asyncio.create_task(self._leader_loop())
    
    async def _leader_loop(self):
        """Loop de líder (envia heartbeats)"""
        
        while self.state == NodeState.LEADER:
            # Envia heartbeats
            for peer in self.cluster_nodes:
                if peer != self.node_id:
                    await self._send_heartbeat(peer)
            
            await asyncio.sleep(self.heartbeat_interval / 1000)
```

**Exemplo de cluster:**
```python
# Criar cluster de 3 nós
nodes = ["node-1", "node-2", "node-3"]

raft_nodes = {
    node_id: RaftNode(node_id, nodes)
    for node_id in nodes
}

# Iniciar todos os nós
for node in raft_nodes.values():
    await node.start()

# Aguardar eleição
await asyncio.sleep(1)

# Verificar líder
leaders = [n for n in raft_nodes.values() if n.state == NodeState.LEADER]
assert len(leaders) == 1
print(f"Líder eleito: {leaders[0].node_id}")
```

#### Load Balancing Inteligente

```python
# src/scaling/intelligent_load_balancer.py (expandir existente)

class WorkloadType(Enum):
    INFERENCE = "inference"
    TRAINING = "training"
    MEMORY_OPS = "memory_ops"
    AGENT_EXECUTION = "agent_execution"

class ClusterLoadBalancer:
    """Balanceador de carga para cluster OmniMind"""
    
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        self.node_metrics: Dict[str, NodeMetrics] = {}
        
    async def select_node(
        self,
        workload_type: WorkloadType,
        requirements: Dict[str, Any]
    ) -> Optional[NodeInfo]:
        """Seleciona melhor nó para workload"""
        
        # Descobre nós capazes
        capability_map = {
            WorkloadType.INFERENCE: "inference",
            WorkloadType.TRAINING: "training",
            WorkloadType.MEMORY_OPS: "memory",
            WorkloadType.AGENT_EXECUTION: "agents"
        }
        
        capability = capability_map[workload_type]
        candidate_nodes = self.registry.discover_service(capability)
        
        if not candidate_nodes:
            return None
        
        # Calcula scores
        scored_nodes = []
        for node in candidate_nodes:
            score = await self._compute_node_score(node, requirements)
            scored_nodes.append((node, score))
        
        # Ordena por score
        scored_nodes.sort(key=lambda x: x[1], reverse=True)
        
        return scored_nodes[0][0] if scored_nodes else None
    
    async def _compute_node_score(
        self,
        node: NodeInfo,
        requirements: Dict[str, Any]
    ) -> float:
        """Computa score do nó"""
        
        score = 1.0
        
        # Penaliza por carga atual
        score *= (1.0 - node.load_factor)
        
        # Bonus por VRAM disponível (se requerido)
        if requirements.get('needs_gpu'):
            metrics = self.node_metrics.get(node.node_id)
            if metrics and metrics.vram_available_gb > 1.0:
                score *= 1.5
        
        # Penaliza por latência
        if node.node_id in self.node_metrics:
            latency_ms = self.node_metrics[node.node_id].avg_latency_ms
            score *= (1.0 / (1.0 + latency_ms / 100.0))
        
        return score
```

**Exemplo de balanceamento:**
```python
balancer = ClusterLoadBalancer(registry)

# Requisição de inferência
node = await balancer.select_node(
    workload_type=WorkloadType.INFERENCE,
    requirements={'needs_gpu': True, 'min_vram_gb': 2.0}
)

if node:
    # Executar no nó selecionado
    result = await execute_on_node(node, inference_task)
```

---

## 🔄 Parte 2: Real-Time Learning

### 2.1 Online Learning Architecture

```python
# src/learning/online_learning_system.py

class OnlineLearningSystem:
    """Sistema de aprendizado em tempo real"""
    
    def __init__(self, base_model: nn.Module):
        self.model = base_model
        self.online_learner = OnlineSGDLearner(base_model)
        self.replay_buffer = PrioritizedReplayBuffer(capacity=10000)
        self.drift_detector = ConceptDriftDetector()
        self.model_manager = ModelVersionManager(base_model)
        
    async def learn_from_stream(
        self,
        data_stream: AsyncIterator[Tuple[torch.Tensor, torch.Tensor]]
    ):
        """Aprende continuamente de stream"""
        
        batch_accumulator = []
        
        async for input_data, target in data_stream:
            # Predição
            with torch.no_grad():
                prediction = self.model(input_data)
            
            # Detecta drift
            drift = self.drift_detector.update(
                prediction.item(),
                target.item()
            )
            
            if drift:
                logger.warning("Concept drift detected!")
                await self._handle_drift()
            
            # Adiciona ao buffer
            self.replay_buffer.add(
                state=input_data,
                action=0,
                reward=compute_reward(prediction, target),
                next_state=input_data,
                done=False,
                priority=compute_priority(prediction, target)
            )
            
            # Acumula para batch
            batch_accumulator.append((input_data, target))
            
            # Update quando batch está cheio
            if len(batch_accumulator) >= 32:
                await self._batch_update(batch_accumulator)
                batch_accumulator = []
    
    async def _batch_update(self, batch: List[Tuple]):
        """Atualização com mini-batch"""
        
        # Combina novo batch com replay
        replay_samples = self.replay_buffer.sample(16)
        
        # Concatena
        all_inputs = torch.stack([b[0] for b in batch] + replay_samples[0])
        all_targets = torch.stack([b[1] for b in batch] + replay_samples[1])
        
        # Update
        loss = self.online_learner.update_batch(all_inputs, all_targets)
        
        logger.debug(f"Batch update: loss={loss:.4f}")
    
    async def _handle_drift(self):
        """Lida com concept drift"""
        
        # Aumenta learning rate temporariamente
        self.online_learner.config.learning_rate *= 2.0
        
        # Aguarda adaptação (10 batches)
        await asyncio.sleep(10)
        
        # Restaura learning rate
        self.online_learner.config.learning_rate /= 2.0
```

**Exemplo de uso:**
```python
# Inicializar sistema
online_system = OnlineLearningSystem(base_model)

# Stream de dados (simulado)
async def data_generator():
    while True:
        # Gera ou lê dados novos
        x = await fetch_new_data()
        y = await fetch_labels(x)
        yield (x, y)
        await asyncio.sleep(0.1)

# Aprender continuamente
stream = data_generator()
await online_system.learn_from_stream(stream)
```

### 2.2 Hot Model Swapping

```python
# src/learning/model_update_manager.py

class ModelUpdateManager:
    """Gerencia updates de modelo sem downtime"""
    
    def __init__(self, base_model: nn.Module):
        self.version_manager = ModelVersionManager(base_model)
        self.continuous_trainer = ContinuousTrainer(self.version_manager)
        self.update_queue = asyncio.Queue()
        
    async def start_continuous_training(self):
        """Inicia treinamento contínuo em background"""
        
        while True:
            # Aguarda intervalo de update (5 minutos)
            await asyncio.sleep(300)
            
            # Coleta dados acumulados
            training_data = await self._collect_training_data()
            
            if len(training_data) > 100:
                # Cria shadow model
                shadow = self.version_manager.create_shadow_copy()
                
                # Treina em background
                await self._train_shadow(shadow, training_data)
                
                # Valida
                is_valid = await self._validate_shadow(shadow)
                
                if is_valid:
                    # Swap atômico (zero downtime)
                    self.version_manager.swap_models()
                    logger.info(f"Model updated to v{self.version_manager.version_counter}")
                else:
                    logger.warning("Shadow model failed validation - keeping current")
    
    async def _train_shadow(
        self,
        shadow_model: nn.Module,
        data: List[Tuple]
    ):
        """Treina shadow model"""
        
        optimizer = torch.optim.Adam(shadow_model.parameters(), lr=0.001)
        shadow_model.train()
        
        for epoch in range(5):
            for batch_x, batch_y in create_batches(data, batch_size=32):
                optimizer.zero_grad()
                outputs = shadow_model(batch_x)
                loss = nn.functional.mse_loss(outputs, batch_y)
                loss.backward()
                optimizer.step()
    
    async def _validate_shadow(self, shadow_model: nn.Module) -> bool:
        """Valida shadow model antes de swap"""
        
        # Testa em validation set
        val_loss = compute_validation_loss(shadow_model, val_data)
        current_loss = compute_validation_loss(
            self.version_manager.active_model,
            val_data
        )
        
        # Aceita se não degradou >5%
        return val_loss <= current_loss * 1.05
```

**Exemplo de deployment contínuo:**
```python
# Iniciar manager
update_manager = ModelUpdateManager(base_model)

# Background task de treinamento contínuo
asyncio.create_task(update_manager.start_continuous_training())

# Servidor continua operacional
# Modelo é atualizado automaticamente a cada 5 minutos
```

---

## 📊 Parte 3: Monitoramento e Observabilidade

### 3.1 Métricas de Cluster

```python
# src/observability/cluster_metrics.py

from prometheus_client import Counter, Gauge, Histogram

# Métricas de cluster
cluster_nodes_total = Gauge(
    'omnimind_cluster_nodes_total',
    'Total de nós no cluster'
)

cluster_requests_total = Counter(
    'omnimind_cluster_requests_total',
    'Total de requisições no cluster',
    ['node_id', 'status']
)

cluster_latency_seconds = Histogram(
    'omnimind_cluster_latency_seconds',
    'Latência de requisições',
    ['node_id']
)

# Métricas de aprendizado
learning_batches_total = Counter(
    'omnimind_learning_batches_total',
    'Total de batches de treinamento'
)

learning_loss = Gauge(
    'omnimind_learning_loss',
    'Loss atual de treinamento'
)

model_version = Gauge(
    'omnimind_model_version',
    'Versão atual do modelo'
)
```

**Exemplo de instrumentação:**
```python
class InstrumentedClusterManager:
    """Cluster manager com métricas"""
    
    async def process_request(self, request):
        # Atualiza gauge
        cluster_nodes_total.set(len(self.registry.nodes))
        
        # Seleciona nó
        node = await self.balancer.select_node(request.workload_type)
        
        # Mede latência
        start = time.time()
        try:
            result = await self.execute_on_node(node, request)
            
            # Incrementa counter de sucesso
            cluster_requests_total.labels(
                node_id=node.node_id,
                status='success'
            ).inc()
            
            return result
            
        except Exception as e:
            # Incrementa counter de erro
            cluster_requests_total.labels(
                node_id=node.node_id,
                status='error'
            ).inc()
            raise
            
        finally:
            # Registra latência
            duration = time.time() - start
            cluster_latency_seconds.labels(
                node_id=node.node_id
            ).observe(duration)
```

### 3.2 Dashboards Grafana

**Configuração de dashboard:**
```yaml
# grafana/dashboards/cluster_overview.json (conceitual)
{
  "dashboard": {
    "title": "OmniMind Cluster Overview",
    "panels": [
      {
        "title": "Cluster Nodes",
        "targets": ["omnimind_cluster_nodes_total"]
      },
      {
        "title": "Request Rate",
        "targets": ["rate(omnimind_cluster_requests_total[5m])"]
      },
      {
        "title": "P95 Latency",
        "targets": ["histogram_quantile(0.95, omnimind_cluster_latency_seconds)"]
      },
      {
        "title": "Model Version",
        "targets": ["omnimind_model_version"]
      }
    ]
  }
}
```

---

## 🧪 Parte 4: Testes e Validação

### 4.1 Testes de Cluster

```python
# tests/scaling/test_cluster_integration.py

import pytest
from src.scaling import (
    ServiceRegistry,
    RaftNode,
    ClusterLoadBalancer
)

class TestClusterIntegration:
    """Testes de integração de cluster"""
    
    @pytest.mark.asyncio
    async def test_node_registration_and_discovery(self):
        """Testa registro e descoberta de nós"""
        
        registry = ServiceRegistry()
        
        # Registra 3 nós
        await registry.register_node("node-1", "192.168.1.10", 8000, ["inference"])
        await registry.register_node("node-2", "192.168.1.11", 8000, ["memory"])
        await registry.register_node("node-3", "192.168.1.12", 8000, ["inference", "memory"])
        
        # Descoberta
        inference_nodes = registry.discover_service("inference")
        assert len(inference_nodes) == 2
        
        memory_nodes = registry.discover_service("memory")
        assert len(memory_nodes) == 2
    
    @pytest.mark.asyncio
    async def test_raft_leader_election(self):
        """Testa eleição de líder"""
        
        nodes = ["node-1", "node-2", "node-3"]
        raft_cluster = {nid: RaftNode(nid, nodes) for nid in nodes}
        
        # Inicia todos
        for node in raft_cluster.values():
            await node.start()
        
        # Aguarda eleição
        await asyncio.sleep(1)
        
        # Verifica que há exatamente 1 líder
        leaders = [n for n in raft_cluster.values() if n.state == NodeState.LEADER]
        assert len(leaders) == 1
    
    @pytest.mark.asyncio
    async def test_load_balancing(self):
        """Testa distribuição de carga"""
        
        registry = ServiceRegistry()
        balancer = ClusterLoadBalancer(registry)
        
        # Registra nós com diferentes cargas
        await registry.register_node("node-1", "192.168.1.10", 8000, ["inference"])
        await registry.register_node("node-2", "192.168.1.11", 8000, ["inference"])
        
        # Simula carga diferente
        registry.nodes["node-1"].load_factor = 0.8
        registry.nodes["node-2"].load_factor = 0.2
        
        # Seleciona nó 100 vezes
        selections = {}
        for _ in range(100):
            node = await balancer.select_node(WorkloadType.INFERENCE, {})
            selections[node.node_id] = selections.get(node.node_id, 0) + 1
        
        # Node 2 deve ser selecionado mais vezes (menor carga)
        assert selections["node-2"] > selections["node-1"]
```

### 4.2 Testes de Online Learning

```python
# tests/learning/test_online_learning_integration.py

class TestOnlineLearningIntegration:
    """Testes de aprendizado online"""
    
    @pytest.mark.asyncio
    async def test_concept_drift_detection(self):
        """Testa detecção de drift"""
        
        detector = ConceptDriftDetector(window_size=100)
        
        # Dados estáveis
        for _ in range(100):
            pred = np.random.normal(0, 1)
            actual = np.random.normal(0, 1)
            drift = detector.update(pred, actual)
            assert not drift
        
        # Muda distribuição
        drift_detected = False
        for _ in range(200):
            pred = np.random.normal(0, 1)
            actual = np.random.normal(5, 1)  # Shift
            drift = detector.update(pred, actual)
            if drift:
                drift_detected = True
                break
        
        assert drift_detected
    
    @pytest.mark.asyncio
    async def test_hot_model_swapping(self):
        """Testa swap de modelos"""
        
        model = create_test_model()
        manager = ModelVersionManager(model)
        
        original_version = manager.version_counter
        
        # Cria shadow
        shadow = manager.create_shadow_copy()
        train_model(shadow, training_data)
        
        # Swap
        manager.swap_models()
        
        assert manager.version_counter == original_version + 1
        assert manager.get_active_model() is shadow
```

---

## ✅ Checklist de Implementação

### Escalabilidade Horizontal
- [ ] NodeRegistry implementado e testado
- [ ] MessageBroker para comunicação inter-nodal
- [ ] RaftConsensus para eleição de líder
- [ ] StateReplicator para consistência
- [ ] ClusterLoadBalancer funcional
- [ ] FailureDetector com recovery automático
- [ ] Testes de integração passando
- [ ] Benchmarks de throughput (target: 3x)

### Real-Time Learning
- [ ] OnlineSGDLearner implementado
- [ ] PrioritizedReplayBuffer funcional
- [ ] ConceptDriftDetector ativo
- [ ] ModelVersionManager com swap atômico
- [ ] ContinuousTrainer em background
- [ ] Testes de drift detection
- [ ] Benchmarks de latência (<100ms)

### Observabilidade
- [ ] Métricas Prometheus configuradas
- [ ] Dashboards Grafana criados
- [ ] Alertas configurados
- [ ] Logging estruturado

---

**Versão:** 1.0  
**Status:** 📋 Documentação Técnica Completa  
**Próximo Documento:** 03_INTELIGENCIA_MULTIMODAL.md
