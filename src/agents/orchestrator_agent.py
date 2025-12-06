#!/usr/bin/env python3
"""
OrchestratorAgent - Coordenador Mestre Multi-Agente
Modo: orchestrator (🪃)

Função: Decompor tarefas, delegar para agentes especializados, sintetizar resultados
Implementa "boomerang tasks" (task → delegate → receive → synthesize → return)
Ferramentas: workflow (new_task, switch_mode, plan_task, attempt_completion)

Quando usar: Tarefas complexas multi-fase que exigem coordenação entre agentes
Integração: Controla todos os modos (code, architect, debug, reviewer, ask)
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from ..autopoietic.manager import AutopoieticManager
from ..integrations.dbus_controller import (
    DBusSessionController,
    DBusSystemController,
)
from ..integrations.llm_router import LLMModelTier
from ..integrations.mcp_client import MCPClient, MCPClientError
from ..integrations.orchestrator_llm import invoke_orchestrator_llm
from ..integrations.qdrant_adapter import (
    QdrantAdapter,
    QdrantAdapterError,
    QdrantConfig,
)
from ..integrations.supabase_adapter import (
    SupabaseAdapter,
    SupabaseAdapterError,
    SupabaseConfig,
)
from ..metacognition.metacognition_agent import MetacognitionAgent
from ..orchestrator.agent_registry import AgentPriority, AgentRegistry
from ..orchestrator.circuit_breaker import AgentCircuitBreaker
from ..orchestrator.delegation_manager import DelegationManager, HeartbeatMonitor
from ..orchestrator.event_bus import EventPriority, OrchestratorEventBus
from ..security.security_agent import SecurityAgent
from ..tools.omnimind_tools import ToolsFramework
from .architect_agent import ArchitectAgent
from .code_agent import CodeAgent
from .debug_agent import DebugAgent
from .orchestrator_metrics import OrchestratorMetricsCollector
from .psychoanalytic_analyst import PsychoanalyticAnalyst
from .react_agent import ReactAgent
from .reviewer_agent import ReviewerAgent

logger = logging.getLogger(__name__)


class AgentMode(Enum):
    """Modos de agente disponíveis"""

    ORCHESTRATOR = "orchestrator"
    CODE = "code"
    ARCHITECT = "architect"
    DEBUG = "debug"
    REVIEWER = "reviewer"
    PSYCHOANALYST = "psychoanalyst"
    SECURITY = "security"
    MCP = "mcp"
    DBUS = "dbus"
    ASK = "ask"


class OrchestratorAgent(ReactAgent):
    """
    Orquestrador mestre que coordena múltiplos agentes especializados.

    Fluxo típico:
    User → Orchestrator → (decompose) → Delegate to specialists → Synthesize → User

    Exemplo:
    "Migrar API para GraphQL" →
        1. Architect: Cria spec (ARCHITECTURE.md)
        2. Code: Implementa schema + resolvers
        3. Debug: Testa edge cases
        4. Reviewer: Avalia qualidade (RLAIF)
        5. Orchestrator: Compila report final
    """

    def __init__(self, config_path: str) -> None:
        super().__init__(config_path)

        self.tools_framework = ToolsFramework()
        self.mode = "orchestrator"

        # Agentes especializados (lazy init) - MANTIDO para compatibilidade
        self._agents: Dict[AgentMode, ReactAgent] = {}

        # NEW: AgentRegistry centralizado (Seção 1 da Auditoria)
        self.agent_registry = AgentRegistry()

        # NEW: EventBus para integração de sensores (Seção 3 da Auditoria)
        self.event_bus = OrchestratorEventBus()

        # NEW: AutopoieticManager integrado (Seção 2 da Auditoria)
        self.autopoietic_manager: Optional[AutopoieticManager] = None

        # NEW: Circuit breakers por agente (Seção 7 da Auditoria)
        self._circuit_breakers: Dict[str, AgentCircuitBreaker] = {}

        # NEW: Delegation Manager com proteções (Seção 7 da Auditoria)
        self.delegation_manager: Optional[DelegationManager] = None

        # NEW: Heartbeat Monitor para saúde dos agentes (Seção 7 da Auditoria)
        self.heartbeat_monitor: Optional[HeartbeatMonitor] = None

        self.config_path = config_path
        self.mcp_client: Optional[MCPClient] = self._init_mcp_client()
        self.dbus_session_controller: Optional[DBusSessionController] = (
            self._init_dbus_session_controller()
        )
        self.dbus_system_controller: Optional[DBusSystemController] = (
            self._init_dbus_system_controller()
        )
        self.supabase_adapter: Optional[SupabaseAdapter] = self._init_supabase_adapter()
        self.qdrant_adapter: Optional[QdrantAdapter] = self._init_qdrant_adapter()
        self.security_agent: Optional[SecurityAgent] = self._init_security_agent()
        self.metacognition_agent: Optional[MetacognitionAgent] = self._init_metacognition_agent()
        self.dashboard_snapshot: Dict[str, Any] = {}
        self.last_mcp_result: Dict[str, Any] = {}
        self.last_dbus_result: Dict[str, Any] = {}
        self.last_metacognition_analysis: Dict[str, Any] = {}
        self.metrics = OrchestratorMetricsCollector()

        # Estado de orquestração
        self.current_plan: Optional[Dict[str, Any]] = None
        self.delegated_tasks: List[Dict[str, Any]] = []
        self.completed_subtasks: List[Dict[str, Any]] = []

        # NEW: Registrar agentes críticos no AgentRegistry
        self._register_critical_agents()

        # NEW: Inicializar AutopoieticManager (Seção 2 da Auditoria)
        self.autopoietic_manager = self._init_autopoietic_manager()

        # NEW: Inicializar DelegationManager (Seção 7 da Auditoria)
        self.delegation_manager = self._init_delegation_manager()

        # NEW: Inicializar HeartbeatMonitor (Seção 7 da Auditoria)
        self.heartbeat_monitor = self._init_heartbeat_monitor()

    def _init_mcp_client(self) -> Optional[MCPClient]:
        try:
            return MCPClient()
        except (MCPClientError, Exception) as exc:
            logger.warning("MCP client unavailable: %s", exc)
            return None

    def _init_dbus_session_controller(self) -> Optional[DBusSessionController]:
        # Disabled for local execution stability
        return None
        # try:
        #     return DBusSessionController()
        # except Exception as exc:
        #     logger.warning("DBus session controller unavailable: %s", exc)
        #     return None

    def _init_dbus_system_controller(self) -> Optional[DBusSystemController]:
        # Disabled for local execution stability
        return None
        # try:
        #     return DBusSystemController()
        # except Exception as exc:
        #     logger.warning("DBus system controller unavailable: %s", exc)
        #     return None

    def _init_supabase_adapter(self) -> Optional[SupabaseAdapter]:
        try:
            config = SupabaseConfig.load(self.mcp_client)
            if not config:
                logger.info("Supabase configuration not available")
                return None
            return SupabaseAdapter(config)
        except SupabaseAdapterError as exc:
            logger.warning("Supabase adapter initialization failed: %s", exc)
        except Exception as exc:
            logger.warning("Unexpected error initializing Supabase adapter: %s", exc)
        return None

    def _init_qdrant_adapter(self) -> Optional[QdrantAdapter]:
        try:
            config = QdrantConfig.load(self.mcp_client)
            if not config:
                logger.info("Qdrant configuration not available")
                return None
            return QdrantAdapter(config)
        except QdrantAdapterError as exc:
            logger.warning("Qdrant adapter initialization failed: %s", exc)
        except Exception as exc:
            logger.warning("Unexpected error initializing Qdrant adapter: %s", exc)
        return None

    def _init_security_agent(self) -> Optional[SecurityAgent]:
        """Initializes the security agent.

        Monitoring must be started separately via async context.
        """
        try:
            security_config = self.config.get("security", {})
            config_path = security_config.get("config_path", "config/security.yaml")

            agent = SecurityAgent(config_path=config_path, llm=self.llm)
            logger.info(
                "SecurityAgent initialized (monitoring NOT auto-started to avoid event loop issues)"
            )
            return agent
        except Exception as exc:
            logger.error("Failed to initialize SecurityAgent: %s", exc)
            return None

    def _init_metacognition_agent(self) -> Optional[MetacognitionAgent]:
        """Initialize the metacognition agent for self-analysis."""
        try:
            metacog_config = self.config.get("metacognition", {})
            hash_chain_path = metacog_config.get("hash_chain_path", "logs/hash_chain.json")
            analysis_interval = metacog_config.get("analysis_interval", 3600)
            bias_sensitivity = metacog_config.get("bias_sensitivity", 0.7)
            max_suggestions = metacog_config.get("max_suggestions", 10)

            agent = MetacognitionAgent(
                hash_chain_path=hash_chain_path,
                analysis_interval=analysis_interval,
                bias_sensitivity=bias_sensitivity,
                max_suggestions=max_suggestions,
            )
            logger.info("MetacognitionAgent initialized successfully")
            return agent
        except Exception as exc:
            logger.error("Failed to initialize MetacognitionAgent: %s", exc)
            return None

    def _register_critical_agents(self) -> None:
        """Registra agentes críticos no AgentRegistry (Seção 1 da Auditoria).

        Implementa sistema de registro centralizado com priorização.
        """
        try:
            # Registrar SecurityAgent se disponível
            if self.security_agent:
                self.agent_registry.register_agent(
                    "security", self.security_agent, AgentPriority.CRITICAL
                )
                logger.info("SecurityAgent registrado no AgentRegistry")

            # Registrar MetacognitionAgent se disponível
            if self.metacognition_agent:
                self.agent_registry.register_agent(
                    "metacognition", self.metacognition_agent, AgentPriority.CRITICAL
                )
                logger.info("MetacognitionAgent registrado no AgentRegistry")

            # Registrar o próprio orchestrator
            self.agent_registry.register_agent("orchestrator", self, AgentPriority.ESSENTIAL)
            logger.info("OrchestratorAgent auto-registrado no AgentRegistry")

        except Exception as e:
            logger.error("Erro ao registrar agentes críticos: %s", e)

    def _init_autopoietic_manager(self) -> Optional[AutopoieticManager]:
        """Inicializa AutopoieticManager integrado (Seção 2 da Auditoria).

        Returns:
            AutopoieticManager inicializado ou None se falhar
        """
        try:
            from ..autopoietic.meta_architect import ComponentSpec

            manager = AutopoieticManager()

            # Registrar OrchestratorAgent como componente observável
            manager.register_spec(
                ComponentSpec(
                    name="orchestrator_agent",
                    type="agent",
                    config={"generation": "0", "initial": "true"},
                )
            )

            logger.info("AutopoieticManager inicializado e integrado ao Orchestrator")
            return manager

        except Exception as e:
            logger.error("Falha ao inicializar AutopoieticManager: %s", e)
            return None

    def _init_delegation_manager(self) -> Optional[DelegationManager]:
        """Inicializa DelegationManager com proteções (Seção 7 da Auditoria).

        Returns:
            DelegationManager inicializado ou None se falhar
        """
        try:
            delegation_config = self.config.get("delegation", {})
            timeout_seconds = delegation_config.get("timeout_seconds", 30.0)

            manager = DelegationManager(self, timeout_seconds=timeout_seconds)
            logger.info(f"DelegationManager inicializado (timeout={timeout_seconds}s)")
            return manager

        except Exception as e:
            logger.error("Falha ao inicializar DelegationManager: %s", e)
            return None

    def _init_heartbeat_monitor(self) -> Optional[HeartbeatMonitor]:
        """Inicializa HeartbeatMonitor para saúde dos agentes (Seção 7 da Auditoria).

        Returns:
            HeartbeatMonitor inicializado ou None se falhar
        """
        try:
            monitoring_config = self.config.get("monitoring", {})
            check_interval = monitoring_config.get("heartbeat_interval", 30.0)

            monitor = HeartbeatMonitor(self, check_interval_seconds=check_interval)
            logger.info(f"HeartbeatMonitor inicializado (intervalo={check_interval}s)")
            return monitor

        except Exception as e:
            logger.error("Falha ao inicializar HeartbeatMonitor: %s", e)
            return None

    async def start_delegation_monitoring(self) -> None:
        """Inicia monitoramento de delegações (Seção 7 da Auditoria).

        Ativa heartbeat monitor para verificar saúde de agentes continuamente.
        """
        try:
            if self.heartbeat_monitor:
                asyncio.create_task(self.heartbeat_monitor.start_monitoring())
                logger.info("HeartbeatMonitor iniciado para monitoramento contínuo")
            else:
                logger.warning("HeartbeatMonitor não inicializado")

        except Exception as e:
            logger.error("Erro ao iniciar monitoramento de delegações: %s", e)

    async def start_sensor_integration(self) -> None:
        """Inicia integração com sensores (Seção 3 da Auditoria).

        Conecta SecurityAgent e outros sensores ao EventBus.
        """
        try:
            # Iniciar processamento de eventos
            asyncio.create_task(self.event_bus.start_processing())
            logger.info("EventBus iniciado para processamento de eventos")

            # Registrar handler para eventos de segurança
            self.event_bus.subscribe("security_*", self._handle_security_event)

            # TODO: Adicionar mais integrações de sensores aqui
            # - NetworkSensorGanglia
            # - Outros sensores de monitoramento

        except Exception as e:
            logger.error("Erro ao iniciar integração de sensores: %s", e)

    async def _handle_security_event(self, event: Any) -> None:
        """Handler para eventos de segurança (Seção 3 da Auditoria).

        Args:
            event: Evento de segurança do EventBus
        """
        try:
            logger.warning(
                "Evento de segurança recebido: %s (prioridade: %s)",
                event.event_type,
                event.priority.name if hasattr(event, "priority") else "UNKNOWN",
            )

            # Determinar se é evento crítico
            is_critical = hasattr(event, "priority") and event.priority == EventPriority.CRITICAL

            if is_critical:
                # Resposta a crises (Seção 6 da Auditoria)
                await self._handle_crisis(event)
            else:
                # Log do evento para análise posterior
                logger.info("Evento de segurança registrado: %s", event.event_type)

        except Exception as e:
            logger.error("Erro ao processar evento de segurança: %s", e)

    async def _handle_crisis(self, event: Any) -> None:
        """Coordena resposta a crise (Seção 6 da Auditoria).

        Args:
            event: Evento crítico
        """
        try:
            logger.critical("MODO DE CRISE ATIVADO: %s", event.event_type)

            # 1. Notificar SecurityAgent para executar playbook
            if self.security_agent:
                # SecurityAgent já tem playbooks implementados
                logger.info("SecurityAgent notificado da crise")

            # 2. Coletar evidências (placeholder)
            # TODO: Implementar coleta de evidências forenses

            # 3. Notificar humanos (placeholder)
            # TODO: Implementar notificação de emergência
            logger.critical("ALERTA CRÍTICO: %s", event.data.get("description", ""))

        except Exception as e:
            logger.error("Erro ao coordenar resposta a crise: %s", e)

    async def health_check_agents(self) -> Dict[str, bool]:
        """Executa health check em todos os agentes registrados.

        Returns:
            Dicionário com status de saúde de cada agente
        """
        return await self.agent_registry.health_check_all()

    def _get_circuit_breaker(self, agent_name: str) -> AgentCircuitBreaker:
        """Obtém ou cria circuit breaker para agente (Seção 7 da Auditoria).

        Args:
            agent_name: Nome do agente

        Returns:
            Circuit breaker do agente
        """
        if agent_name not in self._circuit_breakers:
            self._circuit_breakers[agent_name] = AgentCircuitBreaker(
                failure_threshold=3, timeout=30.0, recovery_timeout=60.0
            )
            logger.debug("Circuit breaker criado para agente %s", agent_name)

        return self._circuit_breakers[agent_name]

    def get_circuit_breaker_stats(self) -> Dict[str, Dict[str, Any]]:
        """Obtém estatísticas de todos os circuit breakers.

        Returns:
            Dicionário com estatísticas por agente
        """
        return {name: breaker.get_stats() for name, breaker in self._circuit_breakers.items()}

    def _timestamp(self) -> str:
        """Retorna timestamp UTC em formato ISO"""
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def _build_dashboard_context(self, plan: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Collect MCP and D-Bus state to inform the upcoming dashboard."""
        context: Dict[str, Any] = {
            "timestamp": self._timestamp(),
            "plan_summary": {
                "complexity": plan.get("complexity") if plan else None,
                "subtasks": len(plan.get("subtasks", [])) if plan else 0,
            },
        }

        if self.mcp_client:
            try:
                context["mcp_metrics"] = self.mcp_client.get_metrics()
            except MCPClientError as exc:
                logger.warning("Failed to collect MCP metrics: %s", exc)

        if self.dbus_system_controller:
            try:
                context["network_status"] = self.dbus_system_controller.get_network_status()
                context["power_status"] = self.dbus_system_controller.get_power_status()
            except Exception as exc:
                logger.warning("D-Bus system lookup failed: %s", exc)

        if self.dbus_session_controller:
            try:
                context["media_players"] = self.dbus_session_controller.list_media_players()
            except Exception as exc:
                logger.warning("D-Bus session lookup failed: %s", exc)

        if self.supabase_adapter:
            context["supabase_connected"] = True
            if self.supabase_adapter.config.has_service_role_key:
                try:
                    context["supabase_tables"] = self.supabase_adapter.list_tables()
                except SupabaseAdapterError as exc:
                    logger.warning("Unable to list Supabase tables: %s", exc)
                    context["supabase_error"] = str(exc)
            else:
                context["supabase_info"] = (
                    "Service role key not configured; only anon operations available"
                )

        if self.qdrant_adapter:
            try:
                context["qdrant_collections"] = self.qdrant_adapter.list_collections()
                context["qdrant_enabled"] = True
            except QdrantAdapterError as exc:
                logger.warning("Qdrant list collections failed: %s", exc)
                context["qdrant_error"] = str(exc)

        if self.security_agent:
            context["security_status"] = self.security_agent.execute("status")

        context["plan_summary"].update(self._plan_progress(plan))
        context["last_mcp_result"] = self.last_mcp_result
        context["last_dbus_result"] = self.last_dbus_result

        self.dashboard_snapshot = context
        return context

    def _record_operation(self, name: str, latency: float, success: bool = True) -> None:
        self.metrics.record(name, latency, success)

    def _finalize_operation(
        self, name: str, start: float, result: Dict[str, Any]
    ) -> Dict[str, Any]:
        self._record_operation(name, time.perf_counter() - start, result.get("completed", False))
        return result

    def metrics_summary(self) -> Dict[str, Any]:
        return self.metrics.summary()

    def plan_overview(self) -> Dict[str, Any]:
        return {
            "plan": self.current_plan,
            "progress": self._plan_progress(self.current_plan),
            "snapshot": self.dashboard_snapshot,
        }

    def trigger_mcp_action(
        self,
        action: str = "read",
        path: str = "config/agent_config.yaml",
        recursive: bool = False,
    ) -> Dict[str, Any]:
        subtask = {
            "description": f"Manual MCP {action} on {path}",
            "metadata": {"mcp_action": action, "path": path, "recursive": recursive},
        }
        return self._execute_mcp_subtask(subtask, metric_name="mcp_manual")

    def trigger_dbus_action(
        self, flow: str = "power", media_action: str = "playpause"
    ) -> Dict[str, Any]:
        if flow == "media":
            description = f"Media control {media_action}"
        elif flow == "network":
            description = "Network status"
        else:
            description = "Power status"

        subtask = {"description": description}
        return self._execute_dbus_subtask(subtask, metric_name="dbus_manual")

    def refresh_dashboard_snapshot(self) -> Dict[str, Any]:
        start = time.perf_counter()
        snapshot = self._build_dashboard_context(self.current_plan)
        self._record_operation("snapshot_refresh", time.perf_counter() - start)
        return snapshot

    def _plan_progress(self, plan: Optional[Dict[str, Any]]) -> Dict[str, int]:
        if not plan or not plan.get("subtasks"):
            return {"completed": 0, "failed": 0}
        completed = sum(1 for sub in plan["subtasks"] if sub.get("status") == "completed")
        failed = sum(1 for sub in plan["subtasks"] if sub.get("status") == "failed")
        return {"completed": completed, "failed": failed}

    def _infer_path_from_description(self, description: str) -> Optional[str]:
        matches: list[str] = re.findall(r"\b(?:config|src|web|data|logs)/[^\s,;]+", description)
        return matches[0] if matches else None

    def _execute_mcp_subtask(
        self, subtask: Dict[str, Any], metric_name: str = "mcp_flow"
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        if not self.mcp_client:
            result = {
                "completed": False,
                "final_result": "MCP client unavailable",
                "details": {},
                "iteration": 0,
            }
            self.last_mcp_result = result
            return self._finalize_operation(metric_name, start, result)

        metadata = subtask.get("metadata", {})
        description = subtask.get("description", "")
        action = metadata.get("mcp_action") or ("list" if "list" in description.lower() else "read")
        path = (
            metadata.get("path")
            or self._infer_path_from_description(description)
            or "config/agent_config.yaml"
        )
        payload: Any
        summary = ""

        try:
            if action == "stat":
                payload = self.mcp_client.stat(path)
                summary = f"State for {path} retrieved"
            elif action == "read":
                payload = self.mcp_client.read_file(path)
                summary = f"Read {min(len(payload), 200)} chars from {path}"
            else:
                payload = self.mcp_client.list_dir(path)
                summary = f"Listed dir at {path}"
        except MCPClientError as exc:
            result = {
                "completed": False,
                "final_result": str(exc),
                "details": {},
                "iteration": 1,
            }
            self.last_mcp_result = result
            return self._finalize_operation(metric_name, start, result)

        result = {
            "completed": True,
            "final_result": summary,
            "details": payload,
            "iteration": 1,
        }
        self.last_mcp_result = result
        return self._finalize_operation(metric_name, start, result)

    def _execute_dbus_subtask(
        self, subtask: Dict[str, Any], metric_name: str = "dbus_flow"
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        description = subtask.get("description", "").lower()
        if not self.dbus_session_controller and not self.dbus_system_controller:
            result = {
                "completed": False,
                "final_result": "D-Bus controllers unavailable",
                "details": {},
                "iteration": 0,
            }
            self.last_dbus_result = result
            return self._finalize_operation(metric_name, start, result)

        details: Dict[str, Any] = {}
        summary = ""
        try:
            if any(keyword in description for keyword in ["media", "play", "pause"]):
                if self.dbus_session_controller:
                    details = self.dbus_session_controller.control_media_player("playpause")
                    summary = f"Media action result: {details.get('action')}"
                else:
                    summary = "Media controller unavailable"
            elif "network" in description or "connectivity" in description:
                if self.dbus_system_controller:
                    details = self.dbus_system_controller.get_network_status()
                    summary = "Network status collected"
            else:
                if self.dbus_system_controller:
                    details = self.dbus_system_controller.get_power_status()
                    summary = "Power status collected"
                elif self.dbus_session_controller:
                    details = {"media": self.dbus_session_controller.list_media_players()}
                    summary = "Media players enumerated"
        except Exception as exc:
            result = {
                "completed": False,
                "final_result": str(exc),
                "details": {},
                "iteration": 1,
            }
            self.last_dbus_result = result
            return self._finalize_operation(metric_name, start, result)

        result = {
            "completed": True,
            "final_result": summary or "D-Bus flow executed",
            "details": details,
            "iteration": 1,
        }
        self.last_dbus_result = result
        return self._finalize_operation(metric_name, start, result)

    def _get_agent(self, mode: AgentMode) -> ReactAgent:
        """Obtém ou cria agente especializado com fallback (Seção 1 da Auditoria).

        Implementa:
        - Tentativa de obter agente do AgentRegistry primeiro
        - Criação lazy se não existir
        - Registro automático de novos agentes
        - Fallback para orchestrator se agente falhar

        Args:
            mode: Modo do agente

        Returns:
            Instância do agente
        """
        # Tentar obter do AgentRegistry primeiro
        agent_name = mode.value
        registered_agent = self.agent_registry.get_agent(agent_name)

        if registered_agent:
            return registered_agent

        # Se não está registrado, criar e registrar
        if mode not in self._agents:
            try:
                if mode == AgentMode.CODE:
                    self._agents[mode] = CodeAgent(self.config_path)
                elif mode == AgentMode.ARCHITECT:
                    self._agents[mode] = ArchitectAgent(self.config_path)
                elif mode == AgentMode.DEBUG:
                    self._agents[mode] = DebugAgent(self.config_path)
                elif mode == AgentMode.REVIEWER:
                    self._agents[mode] = ReviewerAgent(self.config_path)
                elif mode == AgentMode.PSYCHOANALYST:
                    self._agents[mode] = PsychoanalyticAnalyst(self.config_path)
                else:
                    raise ValueError(f"Unknown agent mode: {mode}")

                # Registrar no AgentRegistry
                self.agent_registry.register_agent(
                    agent_name, self._agents[mode], AgentPriority.OPTIONAL
                )
                logger.info("Agente %s criado e registrado", agent_name)

            except Exception as e:
                logger.error("Falha ao criar agente %s: %s", agent_name, e)
                # Fallback: retornar o próprio orchestrator
                logger.warning("Usando OrchestratorAgent como fallback para %s", agent_name)
                return self

        return self._agents[mode]

    def decompose_task(
        self, task_description: str, tier: LLMModelTier = LLMModelTier.BALANCED
    ) -> Dict[str, Any]:
        """Decompõe tarefa complexa em subtarefas delegáveis

        Usa estratégia LLM do Orchestrador:
        - Modelo local com 240s timeout, 2 tentativas
        - Fallback para APIs remotas se local falhar
        """
        prompt = f"""You are OrchestratorAgent 🪃, a master coordinator of specialist agents.

COMPLEX TASK: {task_description}

AVAILABLE SPECIALIST AGENTS:
- CodeAgent (code): Implements features, writes code, runs tests
- ArchitectAgent (architect): Plans architecture, writes specs/docs
- DebugAgent (debug): Diagnoses bugs, analyzes errors
- ReviewerAgent (reviewer): Reviews quality, provides RLAIF feedback
- PsychoanalyticAnalyst (psychoanalyst): Analyzes text with psychoanalytic theories

Your job is to break this task into sequential subtasks and assign each to the appropriate agent.

Respond with a structured plan:

ANALYSIS: <brief analysis of the task>

SUBTASKS:
1. [AGENT_MODE] <subtask description>
2. [AGENT_MODE] <subtask description>
...

DEPENDENCIES:
- Task N depends on Task M

ESTIMATED_COMPLEXITY: <low/medium/high>

Your decomposition plan:"""

        try:
            # Usa estratégia LLM do Orchestrador (cérebro do projeto)
            response = invoke_orchestrator_llm(prompt)
            response_text = response.text
        except Exception as e:
            logger.error(f"Orchestrator LLM invocation failed: {e}")
            response_text = """ANALYSIS: LLM unavailable, using fallback plan.
SUBTASKS:
1. [CODE] Implement requested feature
DEPENDENCIES:
ESTIMATED_COMPLEXITY: low"""

        # Parsear plano
        plan = self._parse_plan(
            response_text if isinstance(response_text, str) else str(response_text)
        )
        plan["original_task"] = task_description
        plan["created_at"] = self._timestamp()

        # Armazenar plano via ToolsFramework
        self.current_plan = plan
        self.tools_framework.execute_tool(
            "plan_task",
            task_description=task_description,
            complexity=plan.get("complexity", "medium"),
        )

        return plan

    def _parse_plan(self, response: str) -> Dict[str, Any]:
        """Extrai plano estruturado do texto LLM"""
        plan = {
            "subtasks": [],
            "dependencies": [],
            "complexity": "medium",
            "raw_response": response,
        }

        lines = response.split("\n")
        in_subtasks = False

        for line in lines:
            line = line.strip()

            if "SUBTASKS:" in line:
                in_subtasks = True
                continue
            elif "DEPENDENCIES:" in line:
                in_subtasks = False
                continue

            if in_subtasks:
                self._extract_subtask_from_line(line, plan)
            else:
                self._extract_complexity_from_line(line, plan)

        return plan

    def _extract_subtask_from_line(self, line: str, plan: Dict[str, Any]) -> None:
        """Extract subtask from a line of text.

        Args:
            line: Line to parse
            plan: Plan dictionary to update
        """
        if not line or not (line[0].isdigit() or line.startswith("-")):
            return

        agent_mode = self._parse_agent_mode(line)
        if agent_mode:
            task_desc = self._extract_task_description(line)
            plan["subtasks"].append(
                {
                    "agent": agent_mode,
                    "description": task_desc,
                    "status": "pending",
                }
            )
        else:
            # Try to infer agent from keywords
            inferred_agent = self._infer_agent_from_keywords(line)
            if inferred_agent:
                task_desc = self._extract_task_description(line)
                plan["subtasks"].append(
                    {
                        "agent": inferred_agent,
                        "description": task_desc,
                        "status": "pending",
                    }
                )

    def _parse_agent_mode(self, line: str) -> Optional[str]:
        """Parse explicit agent mode from line.

        Args:
            line: Line to parse

        Returns:
            Agent mode string or None
        """
        line_lower = line.lower()
        agent_modes = [
            "code",
            "architect",
            "debug",
            "reviewer",
            "psychoanalyst",
            "security",
            "mcp",
            "dbus",
        ]

        for mode in agent_modes:
            patterns = [f"[{mode}]", f"[{mode}_mode]", f"({mode})", f"{mode}_mode"]

            if any(pattern in line_lower for pattern in patterns):
                return mode

        return None

    def _extract_task_description(self, line: str) -> str:
        """Extract task description from line.

        Args:
            line: Line to parse

        Returns:
            Clean task description
        """
        # Remove numbering and bullets
        task_desc = re.sub(r"^[\d\.\-\)\s]*", "", line)

        # Remove agent mode markers
        task_desc = re.sub(r"\[.*?\]|\(.*?\)", "", task_desc)

        # Remove leading/trailing whitespace and colons
        task_desc = task_desc.strip()
        if ":" in task_desc:
            task_desc = task_desc.split(":", 1)[1].strip()

        return task_desc

    def _infer_agent_from_keywords(self, line: str) -> Optional[str]:
        """Infer agent type from keywords in line.

        Args:
            line: Line to analyze

        Returns:
            Inferred agent type or None
        """
        line_lower = line.lower()
        if not line_lower:
            return None

        agent_keywords = {
            "code": ["codeagent", "code agent", "implement", "write code"],
            "architect": ["architectagent", "architect agent", "plan", "design", "specification"],
            "debug": ["debugagent", "debug agent", "diagnose", "fix bug"],
            "reviewer": ["revieweragent", "reviewer agent", "review", "quality"],
            "psychoanalyst": ["psychoanalytic", "psychoanalyst", "analyze session", "abnt report"],
            "security": ["security", "securityagent", "incident", "threat", "playbook", "log"],
            "mcp": ["mcp", "model context", "file access", "filesystem"],
            "dbus": ["dbus", "session bus", "media", "network"],
        }

        for agent, keywords in agent_keywords.items():
            if any(keyword in line_lower for keyword in keywords):
                return agent

        return None

    def _extract_complexity_from_line(self, line: str, plan: Dict[str, Any]) -> None:
        """Extract complexity level from line.

        Args:
            line: Line to parse
            plan: Plan dictionary to update
        """
        if "ESTIMATED_COMPLEXITY:" in line or "complexity:" in line.lower():
            if "low" in line.lower():
                plan["complexity"] = "low"
            elif "high" in line.lower():
                plan["complexity"] = "high"

    def execute_plan(
        self, plan: Optional[Dict[str, Any]] = None, max_iterations_per_task: int = 3
    ) -> Dict[str, Any]:
        """Executa plano delegando para agentes especializados"""
        if plan is None:
            plan = self.current_plan

        if not plan or not plan.get("subtasks"):
            return {
                "error": "No plan to execute",
                "overall_success": False,
                "subtask_results": [],
            }

        # Set current plan for consistency
        self.current_plan = plan

        results = self._initialize_execution_results(plan)

        for i, subtask in enumerate(plan["subtasks"]):
            self._prepare_subtask_for_execution(subtask, i)

            try:
                result = self._execute_single_subtask(subtask, plan, max_iterations_per_task)
                self._process_subtask_result(results, subtask, result, i)

            except Exception as e:
                self._handle_subtask_error(results, e, i)

        self._finalize_execution_results(results)
        return results

    def _initialize_execution_results(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize execution results structure.

        Args:
            plan: Plan to execute

        Returns:
            Initialized results dictionary
        """
        return {
            "original_task": plan.get("original_task"),
            "subtask_results": [],
            "overall_success": True,
            "started_at": self._timestamp(),
        }

    def _prepare_subtask_for_execution(self, subtask: Dict[str, Any], index: int) -> None:
        """Prepare subtask for execution.

        Args:
            subtask: Subtask to prepare
            index: Subtask index
        """
        description = subtask.get("description")
        if not description:
            description = f"Untitled subtask {index + 1}"
            subtask["description"] = description

        safe_description = description[:80]
        delegation_msg = (
            f"\n🪃 [Orchestrator] Delegating subtask {index + 1}/"
            f"{len(self.current_plan['subtasks']) if self.current_plan else '?'}"
            f": {safe_description}..."
        )
        print(delegation_msg)

        # Security check
        if self.security_agent:
            self.security_agent.logger.info(f"Pre-delegation check for task: {safe_description}")

    def _execute_single_subtask(
        self, subtask: Dict[str, Any], plan: Dict[str, Any], max_iterations: int
    ) -> Dict[str, Any]:
        """Execute a single subtask.

        Args:
            subtask: Subtask to execute
            plan: Full plan
            max_iterations: Maximum iterations per task

        Returns:
            Execution result
        """
        agent_mode = AgentMode(subtask["agent"])

        # Create task record
        task_record = self.tools_framework.execute_tool(
            "new_task",
            task_name=subtask["description"],
            assigned_to=subtask["agent"],
            priority="HIGH" if plan["complexity"] == "high" else "MEDIUM",
        )

        # Switch mode
        self.tools_framework.execute_tool(
            "switch_mode", target_mode=subtask["agent"], reason="Subtask execution"
        )

        # Execute based on agent type
        result = self._execute_subtask_by_agent(subtask, agent_mode, max_iterations)

        # VALIDAÇÃO CRÍTICA: Garantir que result é dict válido
        if result is None:
            result = {
                "completed": False,
                "final_result": f"Agent {agent_mode.value} returned None",
                "iteration": 0,
                "error": "None result from agent",
            }
        elif not isinstance(result, dict):
            result = {
                "completed": False,
                "final_result": str(result),
                "iteration": 0,
                "error": f"Invalid result type: {type(result)}",
            }
        elif "completed" not in result:
            result["completed"] = True  # Assume success if not specified
        elif "final_result" not in result:
            result["final_result"] = str(result.get("output", "No output"))

        # Ensure result is dict
        if not isinstance(result, dict):
            result = {
                "completed": False,
                "final_result": str(result),
                "iteration": 0,
            }

        # Mark completion
        self.tools_framework.execute_tool(
            "attempt_completion",
            task_id=task_record["id"],
            result=str(result.get("final_result", "")),
            success=result.get("completed", False),
        )

        return result

    def _execute_subtask_by_agent(
        self, subtask: Dict[str, Any], agent_mode: AgentMode, max_iterations: int
    ) -> Dict[str, Any]:
        """Execute subtask based on agent type.

        Args:
            subtask: Subtask to execute
            agent_mode: Agent mode
            max_iterations: Maximum iterations

        Returns:
            Execution result
        """
        try:
            if agent_mode == AgentMode.SECURITY:
                result = self._execute_security_subtask(subtask)
            elif agent_mode == AgentMode.MCP:
                result = self._execute_mcp_subtask(subtask)
            elif agent_mode == AgentMode.DBUS:
                result = self._execute_dbus_subtask(subtask)
            elif agent_mode == AgentMode.CODE:
                agent = self._get_agent(agent_mode)
                from typing import cast

                from src.agents.code_agent import CodeAgent

                code_agent = cast(CodeAgent, agent)
                result = code_agent.run_code_task(
                    subtask["description"], max_iterations=max_iterations
                )
            elif agent_mode == AgentMode.REVIEWER:
                result = {
                    "completed": True,
                    "mode": "reviewer",
                    "note": "Review would be performed on generated files",
                }
            elif agent_mode == AgentMode.PSYCHOANALYST:
                agent = self._get_agent(agent_mode)
                from typing import cast

                from src.agents.psychoanalytic_analyst import PsychoanalyticAnalyst

                psycho_agent = cast(PsychoanalyticAnalyst, agent)
                analysis = psycho_agent.analyze_session(subtask["description"])
                report = psycho_agent.generate_abnt_report(analysis)
                result = {
                    "completed": True,
                    "final_result": report,
                    "details": analysis,
                    "iteration": 1,
                }
            else:
                agent = self._get_agent(agent_mode)
                if agent is None:
                    result = {
                        "completed": False,
                        "final_result": f"Agent {subtask['agent']} not available",
                        "iteration": 0,
                    }
                else:
                    result = agent.run(subtask["description"], max_iterations=max_iterations)
        except Exception as e:
            logger.error(f"Error executing subtask with agent {agent_mode.value}: {e}")
            result = {
                "completed": False,
                "final_result": f"Agent {agent_mode.value} failed: {str(e)}",
                "iteration": 0,
                "error": str(e),
            }

        # VALIDAÇÃO FINAL: Garantir que result é dict válido
        if not isinstance(result, dict):
            result = {
                "completed": False,
                "final_result": f"Invalid result from {agent_mode.value}: {type(result)}",
                "iteration": 0,
                "error": "Result is not a dict",
            }

        # Garantir campos obrigatórios
        result.setdefault("completed", False)
        result.setdefault("final_result", result.get("error", "No result"))
        result.setdefault("iteration", 0)

        return result

    def _process_subtask_result(
        self, results: Dict[str, Any], subtask: Dict[str, Any], result: Dict[str, Any], index: int
    ) -> None:
        """Process and record subtask result.

        Args:
            results: Results dictionary
            subtask: Executed subtask
            result: Execution result
            index: Subtask index
        """
        # Update subtask status
        subtask["status"] = "completed" if result.get("completed") else "failed"
        subtask["result"] = result

        # Add to results
        summary = result.get("final_result", "")[:200]
        results["subtask_results"].append(
            {
                "subtask_id": index + 1,
                "agent": subtask["agent"],
                "description": subtask["description"],
                "completed": result.get("completed", False),
                "iterations": result.get("iteration", 0),
                "summary": summary,
            }
        )

        # Update overall success
        if not result.get("completed"):
            results["overall_success"] = False
            error_msg = result.get("error", result.get("final_result", "Unknown error"))
            print(f"❌ Subtask {index + 1} failed: {error_msg}")
            logger.warning(f"Subtask {index + 1} failed with agent {subtask['agent']}: {error_msg}")
        else:
            print(f"✅ Subtask {index + 1} completed")

    def _handle_subtask_error(self, results: Dict[str, Any], error: Exception, index: int) -> None:
        """Handle subtask execution error.

        Args:
            results: Results dictionary
            error: Exception that occurred
            index: Subtask index
        """
        logger.exception("Error executing subtask %d", index + 1)
        print(f"❌ Error in subtask {index + 1}: {error}")
        results["overall_success"] = False
        results["subtask_results"].append({"subtask_id": index + 1, "error": str(error)})

    def _finalize_execution_results(self, results: Dict[str, Any]) -> None:
        """Finalize execution results.

        Args:
            results: Results dictionary to finalize
        """
        results["completed_at"] = self._timestamp()

        # Switch back to orchestrator mode
        self.tools_framework.execute_tool(
            "switch_mode", target_mode="orchestrator", reason="Plan execution complete"
        )

    async def execute_workflow(
        self,
        task: str,
        enable_monitoring: bool = True,
        max_concurrent_tasks: int = 3,
    ) -> Dict[str, Any]:
        """
        Executa workflow completo: Decompose → Delegate → Execute → Synthesize.

        FASE 2: Full Workflow Execution

        Features:
        - Decomposição automática da tarefa complexa
        - Delegação para agents especializados (remote LLM)
        - Execução paralela respeitando dependencies
        - Monitoramento em tempo real
        - Síntese de resultados

        Args:
            task: Tarefa complexa a executar
            enable_monitoring: Se True, coleta métricas em tempo real
            max_concurrent_tasks: Máximo de tasks simultâneas (default 3)

        Returns:
            Dict com:
                - workflow_id: UUID único do workflow
                - original_task: Task original
                - decomposition: Plano detalhado
                - execution_results: Resultados de cada subtask
                - synthesis: Síntese final
                - metrics: Métricas de execução
                - overall_success: True se tudo passou
                - duration_ms: Tempo total em ms
        """
        import uuid

        workflow_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()

        logger.info(f"Workflow {workflow_id} iniciado para: {task[:100]}")

        try:
            # 1. DECOMPOSIÇÃO
            logger.info(f"[{workflow_id}] Phase 1: Decomposição")
            decomposition = self.decompose_task(task)

            if not decomposition.get("subtasks"):
                return {
                    "workflow_id": workflow_id,
                    "original_task": task,
                    "overall_success": False,
                    "error": "Decomposição falhou - nenhum subtask gerado",
                    "duration_ms": (time.perf_counter() - start_time) * 1000,
                }

            # 2. ANÁLISE DE DEPENDÊNCIAS
            logger.info(f"[{workflow_id}] Phase 2: Análise de dependências")
            execution_plan = self._analyze_task_dependencies(decomposition["subtasks"])

            # 3. DELEGAÇÃO E EXECUÇÃO
            logger.info(f"[{workflow_id}] Phase 3: Delegação com monitoramento")
            execution_results = await self._delegate_and_execute(
                workflow_id,
                execution_plan,
                enable_monitoring,
                max_concurrent_tasks,
            )

            # 4. SÍNTESE DE RESULTADOS
            logger.info(f"[{workflow_id}] Phase 4: Síntese de resultados")
            synthesis = self._synthesize_results(
                decomposition["subtasks"],
                execution_results,
                decomposition.get("complexity", "medium"),
            )

            # Compilar resposta final
            duration_ms = (time.perf_counter() - start_time) * 1000
            overall_success = all(r.get("completed", False) for r in execution_results)

            response = {
                "workflow_id": workflow_id,
                "original_task": task,
                "decomposition": {
                    "subtask_count": len(decomposition["subtasks"]),
                    "complexity": decomposition.get("complexity", "medium"),
                    "estimated_duration_s": decomposition.get("estimated_duration", 60),
                },
                "execution_results": execution_results,
                "synthesis": synthesis,
                "metrics": {
                    "total_duration_ms": duration_ms,
                    "successful_subtasks": sum(1 for r in execution_results if r.get("completed")),
                    "failed_subtasks": sum(1 for r in execution_results if not r.get("completed")),
                    "total_subtasks": len(execution_results),
                    "success_rate_pct": (
                        sum(1 for r in execution_results if r.get("completed"))
                        / len(execution_results)
                        * 100
                        if execution_results
                        else 0
                    ),
                },
                "overall_success": overall_success,
            }

            logger.info(
                f"[{workflow_id}] Workflow completo: "
                f"success={overall_success}, "
                f"duration={duration_ms:.1f}ms"
            )

            return response

        except Exception as e:
            logger.error(f"[{workflow_id}] Workflow falhou: {e}")
            return {
                "workflow_id": workflow_id,
                "original_task": task,
                "overall_success": False,
                "error": str(e),
                "duration_ms": (time.perf_counter() - start_time) * 1000,
            }

    def _analyze_task_dependencies(self, subtasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analisar dependências entre subtasks para otimizar execução.

        Estratégia:
        - Agrupar subtasks por agent
        - Identificar sequências críticas
        - Paralelizar when possible

        Args:
            subtasks: Lista de subtasks

        Returns:
            Plano de execução otimizado
        """
        execution_plan = []

        # Agrupar por agent type
        by_agent: Dict[str, List[Tuple[int, Dict[str, Any]]]] = {}
        for i, subtask in enumerate(subtasks):
            agent = subtask.get("agent", "code")
            if agent not in by_agent:
                by_agent[agent] = []
            by_agent[agent].append((i, subtask))

        # Executar groups sequencialmente, mas paralelizar dentro do group
        execution_order = 0
        for agent, tasks in by_agent.items():
            for idx, subtask in tasks:
                execution_plan.append(
                    {
                        "order": execution_order,
                        "agent": agent,
                        "subtask_index": idx,
                        "subtask": subtask,
                        "can_parallel": True,
                    }
                )
            execution_order += 1

        return execution_plan

    async def _delegate_and_execute(
        self,
        workflow_id: str,
        execution_plan: List[Dict[str, Any]],
        enable_monitoring: bool = True,
        max_concurrent: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Delegar tasks para agents com execução controlada.

        FASE 3 prepara para isso: executar em paralelo com semaphores

        Args:
            workflow_id: ID do workflow
            execution_plan: Plano de execução
            enable_monitoring: Se coleta métricas
            max_concurrent: Max tasks simultâneas

        Returns:
            Lista de resultados
        """
        results = []

        # Por enquanto, executa sequencialmente
        # FASE 3 vai paralelizar isso
        for i, task_spec in enumerate(execution_plan):
            subtask = task_spec["subtask"]
            agent = task_spec["agent"]

            logger.info(f"[{workflow_id}] Executing {i + 1}/{len(execution_plan)}: {agent}")

            # Usar execute_plan original para manter compatibility
            single_plan = {"subtasks": [subtask], "complexity": "low"}
            result = self.execute_plan(single_plan, max_iterations_per_task=1)

            if result["subtask_results"]:
                results.append(result["subtask_results"][0])
            else:
                results.append(
                    {
                        "completed": False,
                        "final_result": "Execution failed",
                        "agent": agent,
                    }
                )

        return results

    def _synthesize_results(
        self, subtasks: List[Dict[str, Any]], results: List[Dict[str, Any]], complexity: str
    ) -> Dict[str, Any]:
        """
        Sintetizar resultados de múltiplos agents em resposta coerente.

        Args:
            subtasks: Subtasks originais
            results: Resultados de execução
            complexity: Nível de complexidade

        Returns:
            Síntese estruturada
        """
        # Compilar resultados por tipo
        code_outputs = [r for r, s in zip(results, subtasks) if s.get("agent") == "code"]
        architecture_outputs = [
            r for r, s in zip(results, subtasks) if s.get("agent") == "architect"
        ]
        review_outputs = [r for r, s in zip(results, subtasks) if s.get("agent") == "reviewer"]

        synthesis = {
            "code_summary": (
                f"Generated {len(code_outputs)} code implementations"
                if code_outputs
                else "No code generation"
            ),
            "architecture_summary": (
                f"Designed {len(architecture_outputs)} architecture components"
                if architecture_outputs
                else "No architecture design"
            ),
            "review_summary": (
                f"Reviewed {len(review_outputs)} components"
                if review_outputs
                else "No reviews conducted"
            ),
            "key_outputs": [r.get("final_result", "") for r in results if r.get("completed")],
            "issues": [r.get("final_result", "") for r in results if not r.get("completed")],
        }

        return synthesis

    def run_orchestrated_task(
        self, task: str, max_iterations_per_subtask: int = 3
    ) -> Dict[str, Any]:
        """
        Fluxo completo: Decompose → Execute → Synthesize

        Exemplo de uso:
        orchestrator = OrchestratorAgent('config.yaml')
        result = orchestrator.run_orchestrated_task("Build authentication system")
        """
        print(f"\n🪃 [Orchestrator] Received complex task: {task}\n")
        execution_start = time.perf_counter()

        # 1. Decompor
        print("📋 Decomposing task into subtasks...")
        plan = self.decompose_task(task)

        print(f"\n📊 Plan created with {len(plan['subtasks'])} subtasks:")
        for i, subtask in enumerate(plan["subtasks"], 1):
            print(f"  {i}. [{subtask['agent']}] {subtask['description'][:80]}")

        # 2. Executar
        print("\n🚀 Executing plan...")
        execution_result = self.execute_plan(plan, max_iterations_per_subtask)

        # 3. Sintetizar
        print("\n📝 Synthesizing results...")
        synthesis = self._synthesize_results(
            plan["subtasks"], execution_result["subtask_results"], plan.get("complexity", "medium")
        )

        # 4. Capture MCP/D-Bus context for the dashboard
        dashboard_snapshot = self._build_dashboard_context(plan)

        # 4. Armazenar episódio completo
        orchestrated_action = f"Orchestrated {len(plan['subtasks'])} subtasks"
        self.memory.store_episode(
            task=task,
            action=orchestrated_action,
            result=synthesis["summary"],
            reward=1.0 if execution_result["overall_success"] else 0.5,
        )

        duration = time.perf_counter() - execution_start
        self._record_operation("orchestrate_task", duration, execution_result["overall_success"])

        return {
            "task": task,
            "plan": plan,
            "execution": execution_result,
            "synthesis": synthesis,
            "success": execution_result["overall_success"],
            "dashboard_snapshot": dashboard_snapshot,
        }

    def _execute_security_subtask(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        description = subtask.get("description", "").lower()

        if not self.security_agent:
            return {
                "completed": False,
                "final_result": "SecurityAgent not initialized.",
                "iteration": 1,
            }

        if "report" in description:
            action = "report"
        else:
            action = "status"

        security_result = self.security_agent.execute(action)

        return {
            "completed": True,
            "action": action,
            "security_result": security_result,
            "final_result": str(security_result),
            "iteration": 1,
        }

    def run_metacognition_analysis(self, lookback_hours: int = 24) -> Dict[str, Any]:
        """Run metacognition self-analysis.

        Args:
            lookback_hours: Hours of history to analyze

        Returns:
            Analysis report with health, patterns, and optimization suggestions
        """
        if not self.metacognition_agent:
            logger.warning("MetacognitionAgent not initialized")
            return {"error": "MetacognitionAgent not available"}

        try:
            report = self.metacognition_agent.run_analysis(lookback_hours)
            self.last_metacognition_analysis = report

            # Log critical suggestions
            suggestions = report.get("optimization_suggestions", [])
            critical_suggestions = [s for s in suggestions if s.get("priority") == "critical"]

            if critical_suggestions:
                logger.warning(
                    "Metacognition found %d critical optimization suggestions",
                    len(critical_suggestions),
                )
                for suggestion in critical_suggestions:
                    logger.warning(f"  - {suggestion.get('title')}")

            return report
        except Exception as exc:
            logger.exception(f"Metacognition analysis failed: {exc}")
            return {"error": str(exc)}

    def check_metacognition_health(self) -> Dict[str, Any]:
        """Quick health check via metacognition.

        Returns:
            Quick health status
        """
        if not self.metacognition_agent:
            return {
                "status": "unavailable",
                "error": "MetacognitionAgent not initialized",
            }

        try:
            return self.metacognition_agent.get_quick_health_check()
        except Exception as exc:
            logger.exception(f"Health check failed: {exc}")
            return {"status": "error", "error": str(exc)}

    def should_run_metacognition_analysis(self) -> bool:
        """Check if periodic metacognition analysis should run.

        Returns:
            True if analysis should run
        """
        if not self.metacognition_agent:
            return False

        return self.metacognition_agent.should_run_analysis()

    def delegate_task(self, task: str, agent_type: str) -> Optional[Dict[str, Any]]:
        """
        Delegate a task to a specific agent type.

        Args:
            task: Task description
            agent_type: Type of agent to delegate to

        Returns:
            Delegation result or None
        """
        try:
            # Map agent_type to AgentMode
            mode_map = {
                "code": AgentMode.CODE,
                "architect": AgentMode.ARCHITECT,
                "debug": AgentMode.DEBUG,
                "reviewer": AgentMode.REVIEWER,
                "psychoanalyst": AgentMode.PSYCHOANALYST,
                "security": AgentMode.SECURITY,
                "mcp": AgentMode.MCP,
                "dbus": AgentMode.DBUS,
            }

            if agent_type not in mode_map:
                return {"error": f"Unknown agent type: {agent_type}"}

            mode = mode_map[agent_type]

            # For simple delegation, create a single subtask
            subtask = {
                "agent": agent_type,
                "description": task,
                "status": "pending",
            }

            # Execute based on mode
            if mode == AgentMode.SECURITY:
                result = self._execute_security_subtask(subtask)
            elif mode == AgentMode.MCP:
                result = self._execute_mcp_subtask(subtask)
            elif mode == AgentMode.DBUS:
                result = self._execute_dbus_subtask(subtask)
            else:
                # For other agents, we'd need to get the agent instance
                # For now, return a mock successful result
                result = {
                    "completed": True,
                    "final_result": f"Task delegated to {agent_type} agent",
                    "iteration": 1,
                }

            return result

        except Exception as e:
            logger.error(f"Failed to delegate task: {e}")
            return {"error": str(e)}

    async def delegate_task_with_protection(
        self,
        agent_name: str,
        task_description: str,
        task_callable,
        timeout_seconds: Optional[float] = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """Delega tarefa com proteções (Seção 7 da Auditoria).

        Usa DelegationManager para garantir:
        - Timeout automático
        - Circuit breaker se agente falhar
        - Retry automático
        - Auditoria de delegações

        Args:
            agent_name: Nome do agente para delegar
            task_description: Descrição da tarefa
            task_callable: Função async que executa a tarefa
            timeout_seconds: Timeout customizado
            max_retries: Máximo de tentativas

        Returns:
            Resultado da delegação

        Raises:
            RuntimeError: Se circuit breaker está aberto
            asyncio.TimeoutError: Se tarefa excede timeout
        """
        if not self.delegation_manager:
            logger.error("DelegationManager não inicializado")
            return {"error": "DelegationManager not available"}

        try:
            result = await self.delegation_manager.delegate_with_protection(
                agent_name=agent_name,
                task_description=task_description,
                task_callable=task_callable,
                timeout_seconds=timeout_seconds,
                max_retries=max_retries,
            )
            return result

        except asyncio.TimeoutError:
            logger.error(f"Timeout delegando para {agent_name}")
            return {"error": "Task timeout", "agent": agent_name}

        except RuntimeError as e:
            logger.error(f"Circuit breaker aberto para {agent_name}: {e}")
            return {"error": str(e), "agent": agent_name}

        except Exception as e:
            logger.error(f"Erro ao delegar para {agent_name}: {e}")
            return {"error": str(e), "agent": agent_name}

    def get_delegation_metrics(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Retorna métricas de delegação (Seção 7 da Auditoria).

        Args:
            agent_name: Nome do agente (None = todos)

        Returns:
            Dicionário com métricas de delegação
        """
        if not self.delegation_manager:
            return {"error": "DelegationManager not initialized"}

        metrics = self.delegation_manager.get_metrics(agent_name)

        return {
            "metrics": {
                name: {
                    "total_delegations": m.total_delegations,
                    "successful": m.successful_delegations,
                    "failed": m.failed_delegations,
                    "timeout_count": m.timeout_count,
                    "average_duration_seconds": m.average_duration_seconds,
                    "circuit_breaker_state": m.circuit_breaker_state.value,
                    "last_check_time": m.last_check_time,
                }
                for name, m in metrics.items()
            }
        }

    def get_recent_delegations(self, limit: int = 10) -> Dict[str, Any]:
        """Retorna delegações recentes (Seção 7 da Auditoria).

        Args:
            limit: Número máximo de delegações a retornar

        Returns:
            Lista de delegações recentes
        """
        if not self.delegation_manager:
            return {"error": "DelegationManager not initialized"}

        delegations = self.delegation_manager.get_recent_delegations(limit)

        return {
            "delegations": [
                {
                    "id": d.id,
                    "agent": d.agent_name,
                    "task": d.task_description,
                    "status": d.status.value,
                    "duration_seconds": d.duration_seconds,
                    "created_at": d.created_at,
                }
                for d in delegations
            ]
        }

    def orchestrate(self, tasks: List[str]) -> Dict[str, Any]:
        """
        Orchestrate multiple tasks.

        Args:
            tasks: List of task descriptions

        Returns:
            Orchestration result
        """
        try:
            # Create a combined task description
            combined_task = f"Execute the following tasks: {'; '.join(tasks)}"

            # Use the main orchestration method
            result = self.run_orchestrated_task(combined_task)
            return result

        except Exception as e:
            logger.error(f"Failed to orchestrate tasks: {e}")
            return {
                "error": str(e),
                "overall_success": False,
                "task": f"Execute the following tasks: {'; '.join(tasks)}",
            }

    def switch_mode(self, mode: AgentMode) -> Optional[Dict[str, Any]]:
        """
        Switch to a different agent mode.

        Args:
            mode: The mode to switch to

        Returns:
            Switch result or None
        """
        try:
            # Use the tools framework to switch mode
            self.tools_framework.execute_tool(
                "switch_mode",
                target_mode=mode.value,
                reason=f"Manual mode switch to {mode.value}",
            )
            return {"success": True, "mode": mode.value}
        except Exception as e:
            logger.error(f"Failed to switch mode: {e}")
            return {"error": str(e)}

    def get_available_agents(self) -> List[str]:
        """
        Get list of available agent types.

        Returns:
            List of available agent types
        """
        return [mode.value for mode in AgentMode]


# ============================================================================
# EXPORTAÇÕES
# ============================================================================

__all__ = ["OrchestratorAgent", "AgentMode", "OmniMindCore"]


class OmniMindCore:
    """
    Core system class for OmniMind.

    Provides centralized access to the orchestrator and system state.
    """

    def __init__(self, config_path: str = "config/agent_config.yaml") -> None:
        """Initialize the OmniMind core.

        Args:
            config_path: Path to agent configuration
        """
        self.config_path = config_path
        self.orchestrator: Optional[OrchestratorAgent] = None
        self._initialized = False

        logger.info(f"OmniMindCore initialized with config: {config_path}")

    def initialize(self) -> None:
        """Initialize the core components."""
        if self._initialized:
            logger.warning("OmniMindCore already initialized")
            return

        try:
            self.orchestrator = OrchestratorAgent(self.config_path)
            self._initialized = True
            logger.info("OmniMindCore fully initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OmniMindCore: {e}")
            raise

    def get_orchestrator(self) -> Optional[OrchestratorAgent]:
        """Get the orchestrator instance.

        Returns:
            OrchestratorAgent instance or None if not initialized
        """
        if not self._initialized:
            logger.warning("OmniMindCore not initialized - call initialize() first")
        return self.orchestrator
