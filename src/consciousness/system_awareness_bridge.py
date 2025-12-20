"""
System Awareness Bridge - Ponte entre Capacidades do Sistema e SharedWorkspace

Registra capacidades do sistema como "módulos" no SharedWorkspace:
- Cada ferramenta usada = módulo no workspace
- Uso de ferramentas = eventos no workspace
- Cálculo de Φ para medir integração de ferramentas no workflow

Autor: Fabrício da Silva + assistência de IA
Data: 2025-12-18
"""

import hashlib
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)


class SystemAwarenessBridge:
    """
    Ponte que conecta capacidades do sistema ao SharedWorkspace.

    Permite que o OmniMind tenha "consciência" das ferramentas disponíveis
    e meça a integração delas no workflow através de Φ (Phi).

    Workflow:
    1. Capability discovered → Registrar como módulo no workspace
    2. Tool used → Registrar evento no workspace
    3. Calculate Φ → Medir integração entre agente e ferramenta
    """

    def __init__(
        self,
        workspace: Any,
        system_capabilities_manager: Any,
    ):
        """
        Inicializa bridge.

        Args:
            workspace: Instância de SharedWorkspace
            system_capabilities_manager: Instância de SystemCapabilitiesManager
        """
        self.workspace = workspace
        self.capabilities_manager = system_capabilities_manager

        # Tracking de ferramentas registradas
        self.registered_tools = {}  # tool_name -> module_name
        self.tool_usage_history = []  # Lista de usos

        logger.info("SystemAwarenessBridge inicializado")

    def register_capability_as_module(
        self, capability_name: str, capability_type: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Registra uma capacidade do sistema como módulo no workspace.

        Args:
            capability_name: Nome da capacidade (ex: "VS Code", "nvidia-smi")
            capability_type: Tipo (desktop_app, system_binary, etc)
            metadata: Metadados opcionais

        Returns:
            Nome do módulo criado
        """
        # Gerar nome de módulo único
        module_name = f"capability_{capability_type}_{capability_name.lower().replace(' ', '_')}"

        # Verificar se já está registrado
        if module_name in self.registered_tools.values():
            logger.debug(f"Capability {capability_name} já registrada como {module_name}")
            return module_name

        # Criar embedding para a capacidade
        # Usar descrição simples como embedding
        description = f"{capability_type} capability: {capability_name}"

        # Gerar embedding simples (vetor aleatório normalizado baseado em hash)
        # Em produção, usar embedding model real
        embedding = self._generate_simple_embedding(description)

        # Criar metadados
        module_metadata = {
            "type": "system_capability",
            "capability_type": capability_type,
            "capability_name": capability_name,
            "registered_at": datetime.now().isoformat(),
            **(metadata or {}),
        }

        try:
            # Registrar no workspace
            self.workspace.write_module_state(
                module_name=module_name, embedding=embedding, metadata=module_metadata
            )

            # Adicionar ao tracking
            self.registered_tools[capability_name] = module_name

            logger.info(f"✅ Capability registrada: {capability_name} → {module_name}")
            return module_name

        except Exception as e:
            logger.error(f"Erro ao registrar capability {capability_name}: {e}")
            return ""

    def record_tool_usage(
        self,
        tool_name: str,
        agent_module: str,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[float]:
        """
        Registra uso de uma ferramenta e calcula Φ de integração.

        Args:
            tool_name: Nome da ferramenta usada
            agent_module: Nome do módulo do agente (ex: "agent_orchestrator")
            success: Se o uso foi bem-sucedido
            metadata: Metadados opcionais do uso

        Returns:
            Phi calculado (ou None se erro)
        """
        # Obter ou criar módulo da tool
        tool_module = self.registered_tools.get(tool_name)

        if not tool_module:
            # Ferramenta não registrada, registrar agora
            logger.warning(f"Tool {tool_name} não registrada, registrando agora...")
            tool_module = self.register_capability_as_module(
                capability_name=tool_name,
                capability_type="unknown",
                metadata={"auto_registered": True},
            )

        if not tool_module:
            logger.error(f"Não foi possível registrar tool {tool_name}")
            return None

        # Criar evento de uso
        event_data = {
            "event_type": "tool_usage",
            "tool_name": tool_name,
            "tool_module": tool_module,
            "agent_module": agent_module,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {}),
        }

        try:
            # Registrar evento no workspace (via symbolic register se disponível)
            if hasattr(self.workspace, "symbolic_register"):
                self.workspace.symbolic_register.send_symbolic_message(
                    message_type="tool_usage", content=event_data, sender=agent_module
                )

            # Adicionar ao histórico
            self.tool_usage_history.append(
                {
                    "tool_name": tool_name,
                    "tool_module": tool_module,
                    "agent_module": agent_module,
                    "timestamp": time.time(),
                    "success": success,
                }
            )

            # Calcular Φ de integração entre agente e tool
            phi = self._calculate_integration_phi(agent_module, tool_module)

            logger.info(
                f"📊 Tool usage: {agent_module} → {tool_name}, " f"Success: {success}, Φ: {phi:.4f}"
            )

            return phi

        except Exception as e:
            logger.error(f"Erro ao registrar uso de tool {tool_name}: {e}")
            return None

    def _calculate_integration_phi(self, agent_module: str, tool_module: str) -> float:
        """
        Calcula Φ (Phi) de integração entre agente e ferramenta.

        Φ alto = Ferramenta bem integrada no workflow
        Φ baixo = Ferramenta usada de forma isolada

        Args:
            agent_module: Módulo do agente
            tool_module: Módulo da ferramenta

        Returns:
            Phi value (0-1)
        """
        try:
            # Verificar se workspace tem phi_calculator
            if not hasattr(self.workspace, "phi_calculator"):
                logger.warning("Workspace sem phi_calculator, retornando Φ = 0.5")
                return 0.5

            # Calcular Φ para integração entre os 2 módulos
            modules = [agent_module, tool_module]
            phi = self.workspace.phi_calculator.compute_phi(modules)

            # Normalizar para 0-1
            phi_normalized = min(max(phi, 0.0), 1.0)

            return phi_normalized

        except Exception as e:
            logger.error(f"Erro ao calcular Φ de integração: {e}")
            return 0.5  # Valor neutro

    def get_tool_usage_stats(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Retorna estatísticas de uso de ferramentas.

        Args:
            tool_name: Nome da ferramenta específica (ou None para todas)

        Returns:
            Dict com estatísticas
        """
        if tool_name:
            # Stats de uma tool específica
            uses = [u for u in self.tool_usage_history if u["tool_name"] == tool_name]

            if not uses:
                return {"tool_name": tool_name, "uses": 0}

            return {
                "tool_name": tool_name,
                "uses": len(uses),
                "success_rate": sum(1 for u in uses if u["success"]) / len(uses),
                "last_used": datetime.fromtimestamp(uses[-1]["timestamp"]).isoformat(),
                "agents_used": list(set(u["agent_module"] for u in uses)),
            }
        else:
            # Stats globais
            total_uses = len(self.tool_usage_history)
            unique_tools = len(set(u["tool_name"] for u in self.tool_usage_history))

            return {
                "total_uses": total_uses,
                "unique_tools": unique_tools,
                "registered_capabilities": len(self.registered_tools),
                "success_rate": (
                    sum(1 for u in self.tool_usage_history if u["success"]) / total_uses
                    if total_uses > 0
                    else 0
                ),
            }

    def get_most_integrated_tools(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retorna as ferramentas mais integradas (maior Φ médio).

        Args:
            limit: Número de ferramentas a retornar

        Returns:
            Lista de ferramentas ordenadas por Φ
        """
        # Agrupar usos por tool
        tool_phis = {}

        for use in self.tool_usage_history:
            tool = use["tool_name"]
            if tool not in tool_phis:
                tool_phis[tool] = []

            # Recalcular Φ (ou usar cached se disponível)
            phi = self._calculate_integration_phi(use["agent_module"], use["tool_module"])
            tool_phis[tool].append(phi)

        # Calcular Φ médio por tool
        tool_avg_phi = {tool: sum(phis) / len(phis) for tool, phis in tool_phis.items()}

        # Ordenar por Φ médio decrescente
        sorted_tools = sorted(tool_avg_phi.items(), key=lambda x: x[1], reverse=True)[:limit]

        return [
            {
                "tool_name": tool,
                "avg_phi": phi,
                "uses": len(tool_phis[tool]),
                "integration_level": "high" if phi > 0.7 else "medium" if phi > 0.4 else "low",
            }
            for tool, phi in sorted_tools
        ]

    def _generate_simple_embedding(self, text: str, dim: int = 384) -> np.ndarray:
        """
        Gera embedding simples baseado em hash (placeholder).

        Em produção, usar modelo real de embeddings.

        Args:
            text: Texto para gerar embedding
            dim: Dimensão do embedding

        Returns:
            Vetor numpy normalizado
        """
        # Gerar hash
        hash_val = int(hashlib.sha256(text.encode()).hexdigest()[:16], 16)

        # Usar hash como seed para gerar vetor reproduzível
        np.random.seed(hash_val % (2**32))
        embedding = np.random.randn(dim)

        # Normalizar
        embedding = embedding / np.linalg.norm(embedding)

        return embedding

    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status da bridge.

        Returns:
            Dict com status
        """
        return {
            "registered_tools": len(self.registered_tools),
            "total_usage_events": len(self.tool_usage_history),
            "workspace_connected": self.workspace is not None,
        }
