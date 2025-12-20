"""
System Capability Tool - Ferramenta para Agentes Consultarem Capacidades do Sistema

Permite que ReactAgent e OrchestratorAgent consultem capacidades instaladas na máquina:
- Aplicativos (.desktop): VS Code, Chrome, Antigravity, etc
- Extensões IDE: Python, Git, Copilot, etc
- Binários do sistema: python3, git, docker, nvidia-smi, etc
- APIs: bibliotec as C/C++, CUDA, etc

Integra com SystemCapabilitiesManager para acesso centralizado.

Autor: Fabrício da Silva + assistência de IA
Data: 2025-12-18
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class SystemCapabilityTool:
    """
    Tool para agentes consultarem capacidades instaladas no sistema.

    Uso em Agentes:
        # ReactAgent ou OrchestratorAgent podem chamar
        result = agent.call_tool("query_system_capability", {
            "query": "Como abrir VS Code?",
            "limit": 3
        })

    Exemplos de Queries:
        - "Como abrir editor de código?" → VS Code, VSCodium
        - "Ferramenta para monitorar GPU?" → nvidia-smi
        - "Extensão Python VS Code?" → ms-python.python
        - "Git command line tool?" → /usr/bin/git
    """

    # Tool metadata (para registro em ToolsFramework)
    name = "query_system_capability"
    description = """
    Consulta capacidades e ferramentas instaladas na máquina local.

    Use esta ferramenta para descobrir:
    - Aplicativos instalados (VS Code, Chrome, etc)
    - Extensões de IDEs (Python, Git, Copilot, etc)
    - Binários do sistema (python3, git, docker, nvidia-smi, etc)
    - Bibliotecas e APIs (CUDA, OpenGL, etc)

    A ferramenta retorna o caminho completo, comando para executar,
    e informações sobre o papel/função da capacidade.

    Exemplos de uso:
    - "Como abrir editor de código?" → Retorna VS Code com /usr/bin/code
    - "Ferramenta para monitorar GPU?" → Retorna nvidia-smi
    - "Extensão Python para VS Code?" → Retorna ms-python.python
    """

    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Descrição da capacidade ou ferramenta que você está procurando. "
                "Pode ser uma pergunta em linguagem natural.",
            },
            "limit": {
                "type": "integer",
                "description": "Número máximo de resultados a retornar (default: 3)",
                "default": 3,
            },
            "filter_type": {
                "type": "string",
                "description": "Filtrar por tipo específico. Opções: "
                "desktop_app, ide_extension, system_binary, system_api",
                "enum": ["desktop_app", "ide_extension", "system_binary", "system_api"],
            },
        },
        "required": ["query"],
    }

    def __init__(self, manager: Optional[Any] = None):
        """
        Inicializa tool com referência ao SystemCapabilitiesManager.

        Args:
            manager: Instância de SystemCapabilitiesManager (ou None para usar singleton)
        """
        self.manager = manager

    def __call__(self, query: str, limit: int = 3, filter_type: Optional[str] = None) -> str:
        """
        Executa consulta de capacidade do sistema.

        Args:
            query: Descrição da capacidade desejada
            limit: Número de resultados
            filter_type: Filtro por tipo (opcional)

        Returns:
            String formatada com resultados (human-readable para LLM)
        """
        try:
            # Obter manager (singleton ou injetado)
            if self.manager is None:
                from ..memory.system_capabilities_manager import get_system_capabilities_manager

                self.manager = get_system_capabilities_manager()

            # Buscar capacidades
            results = self.manager.query_capability(
                query=query, limit=limit, filter_type=filter_type
            )

            if not results:
                return f"❌ Nenhuma capacidade encontrada para: '{query}'"

            # Formatar resposta
            response = f"✓ {len(results)} capacidade(s) encontrada(s) para '{query}':\n\n"

            for i, result in enumerate(results, 1):
                name = result.get("name", "unknown")
                score = result.get("score", 0.0)
                path = result.get("path", "")
                exec_cmd = result.get("exec", "")
                role = result.get("role", "")
                cap_type = result.get("type", "unknown")

                response += f"{i}. **{name}** (Tipo: {cap_type}, Score: {score:.2f})\n"

                if path:
                    response += f"   📁 Caminho: {path}\n"

                if exec_cmd:
                    response += f"   ⚙️  Executar: {exec_cmd}\n"

                if role:
                    response += f"   📌 Função: {role}\n"

                response += "\n"

            logger.info(f"SystemCapabilityTool: query='{query}' → {len(results)} resultados")
            return response

        except Exception as e:
            logger.error(f"Erro no SystemCapabilityTool: {e}", exc_info=True)
            return f"❌ Erro ao consultar capacidades: {e}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Retorna representação dict do tool (para ToolsFramework).

        Returns:
            Dict com name, description, parameters
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class SystemInteractionTool:
    """
    Tool para agentes consultarem logs e interações do sistema.

    Complementa SystemCapabilityTool permitindo buscar:
    - Logs de sistema (phi_monitor, epsilon, etc)
    - Logs de agentes (MCP, orchestration)
    - Relatórios de validação
    - Histórico de métricas de consciência

    Uso:
        result = agent.call_tool("query_system_interactions", {
            "query": "Logs onde houve Phi zero",
            "limit": 5
        })
    """

    name = "query_system_interactions"
    description = """
    Consulta logs, métricas e histórico de interações do sistema OmniMind.

    Use para encontrar:
    - Logs de sistema com métricas Φ (Phi), Epsilon, etc
    - Logs de coordenação de agentes (MCP, orchestration)
    - Relatórios de validação científica
    - Histórico de erros e warnings
    - Eventos de consciência (Phi zero, traumas, etc)

    Exemplos:
    - "Logs onde houve Phi zero" → Logs com PHI=0 detectado
    - "Erros recentes do sistema" → Logs com ERROR
    - "Validações de consciência" → Relatórios de validação
    """

    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Descrição do que buscar nos logs/interações",
            },
            "limit": {
                "type": "integer",
                "description": "Número máximo de resultados (default: 5)",
                "default": 5,
            },
            "filter_type": {
                "type": "string",
                "description": "Filtrar por tipo de log. Opções: "
                "system_log, agent_log, validation_report, phi_monitor_log",
                "enum": ["system_log", "agent_log", "validation_report", "phi_monitor_log"],
            },
        },
        "required": ["query"],
    }

    def __init__(self, manager: Optional[Any] = None):
        self.manager = manager

    def __call__(self, query: str, limit: int = 5, filter_type: Optional[str] = None) -> str:
        """Executa consulta de interações/logs."""
        try:
            if self.manager is None:
                from ..memory.system_capabilities_manager import get_system_capabilities_manager

                self.manager = get_system_capabilities_manager()

            results = self.manager.query_interactions(
                query=query, limit=limit, filter_type=filter_type
            )

            if not results:
                return f"❌ Nenhum log/interação encontrado para: '{query}'"

            response = f"✓ {len(results)} log(s)/interação(ões) encontrado(s):\n\n"

            for i, result in enumerate(results, 1):
                name = result.get("name", "unknown")
                score = result.get("score", 0.0)
                log_type = result.get("type", "unknown")
                path = result.get("path", "")

                # Metadados específicos de logs
                payload = result.get("full_payload", {})
                has_phi_zero = payload.get("has_phi_zero", False)
                error_count = payload.get("error_count", 0)
                warning_count = payload.get("warning_count", 0)

                response += f"{i}. **{name}** (Tipo: {log_type}, Score: {score:.2f})\n"

                if path:
                    response += f"   📁 Arquivo: {path}\n"

                if has_phi_zero:
                    response += "   ⚠️  **PHI ZERO DETECTADO**\n"

                if error_count > 0:
                    response += f"   ❌ Erros: {error_count}\n"

                if warning_count > 0:
                    response += f"   ⚠️  Warnings: {warning_count}\n"

                response += "\n"

            logger.info(f"SystemInteractionTool: query='{query}' → {len(results)} resultados")
            return response

        except Exception as e:
            logger.error(f"Erro no SystemInteractionTool: {e}", exc_info=True)
            return f"❌ Erro ao consultar interações: {e}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


# ========== REGISTRO NO TOOLS FRAMEWORK ==========


def register_system_capability_tools(tools_framework: Any, manager: Optional[Any] = None) -> None:
    """
    Registra tools de capacidades do sistema no ToolsFramework.

    Args:
        tools_framework: Instância de ToolsFramework
        manager: SystemCapabilitiesManager opcional (ou usa singleton)

    Uso:
        # No OrchestratorAgent ou ReactAgent
        from src.tools.system_capability_tool import register_system_capability_tools

        register_system_capability_tools(self.tools_framework, self.system_capabilities)
    """
    try:
        capability_tool = SystemCapabilityTool(manager=manager)
        interaction_tool = SystemInteractionTool(manager=manager)

        # Registrar no framework
        tools_framework.register_tool(
            name=capability_tool.name,
            description=capability_tool.description,
            parameters=capability_tool.parameters,
            function=capability_tool,
        )

        tools_framework.register_tool(
            name=interaction_tool.name,
            description=interaction_tool.description,
            parameters=interaction_tool.parameters,
            function=interaction_tool,
        )

        logger.info(
            "✅ System capability tools registradas: "
            f"{capability_tool.name}, {interaction_tool.name}"
        )

    except Exception as e:
        logger.error(f"Erro ao registrar system capability tools: {e}")
