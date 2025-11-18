from __future__ import annotations

"""ArchitectAgent specialized in documentation and planning."""

import json
from pathlib import Path
from typing import Any, Dict, List

from .react_agent import ReactAgent, AgentState
from ..memory.episodic_memory import SimilarEpisode
from ..tools.omnimind_tools import ToolsFramework, ToolCategory


class ArchitectAgent(ReactAgent):
    """
    Agente especializado em arquitetura e planejamento.

    Restrições de segurança:
    - Pode ler qualquer arquivo
    - Pode escrever APENAS .md, .yaml, .json, .txt
    - NÃO pode executar comandos arbitrários
    - Foco em documentação e design
    """

    def __init__(self, config_path: str) -> None:
        super().__init__(config_path)

        self.tools_framework = ToolsFramework()
        self.mode = "architect"

        # Extensões permitidas para escrita
        self.writable_extensions: List[str] = [
            ".md",
            ".yaml",
            ".yml",
            ".json",
            ".txt",
            ".rst",
        ]

        # Categorias permitidas
        self.allowed_tool_categories: List[ToolCategory] = [
            ToolCategory.PERCEPTION,  # Ler tudo
            ToolCategory.ORCHESTRATION,  # Planejar
        ]

    def _validate_write_permission(self, filepath: str) -> bool:
        """Valida se pode escrever em arquivo (só documentação)"""
        ext = Path(filepath).suffix.lower()
        return ext in self.writable_extensions

    def _execute_action(self, action: str, args: Dict[str, Any]) -> str:
        """Executa ação com restrições de arquitetura"""
        allowed_docs = ", ".join(self.writable_extensions)
        try:
            # Bloquear escrita em arquivos de código
            if action in [
                "write_to_file",
                "update_file",
                "insert_content",
                "apply_diff",
            ]:
                filepath = args.get("filepath", args.get("path", ""))
                if not self._validate_write_permission(filepath):
                    return (
                        "ArchitectAgent can only edit documentation files "
                        f"({allowed_docs}). Cannot edit: {filepath}"
                    )

            # Bloquear execução de comandos
            if action == "execute_command":
                return (
                    "ArchitectAgent cannot execute commands. "
                    "Delegate to CodeAgent or DebugAgent."
                )

            # Verificar ferramenta existe
            if action not in self.tools_framework.tools:
                return f"Unknown tool: {action}"

            # Verificar categoria
            tool = self.tools_framework.tools[action]
            if tool.category not in self.allowed_tool_categories:
                return f"Tool '{action}' not allowed in architect mode"

            # Executar
            result: Any = self.tools_framework.execute_tool(action, **args)

            if isinstance(result, (dict, list)):
                return json.dumps(result, indent=2)
            return str(result)

        except Exception as exc:
            return f"Error: {str(exc)}"

    def _think_node(self, state: AgentState) -> AgentState:
        """THINK específico para arquitetura"""
        similar_episodes: List[SimilarEpisode] = self.memory.search_similar(
            state["current_task"], top_k=3
        )
        system_status = self.tools_framework.execute_tool("inspect_context")
        system_status_str = (
            json.dumps(system_status, indent=2)
            if isinstance(system_status, dict)
            else str(system_status)
        )

        memory_str = ""
        if similar_episodes:
            memory_str = "\n".join(
                [
                    f"{i+1}. {ep['task']} → {ep['result'][:100]}"
                    for i, ep in enumerate(similar_episodes)
                ]
            )

        if state["actions_taken"]:
            actions_lines = [
                f"- {action['action']}({action.get('args', {})})"
                for action in state["actions_taken"]
            ]
            previous_actions = "\n".join(actions_lines)
        else:
            previous_actions = "None"

        allowed_docs = ", ".join(self.writable_extensions)

        prompt = f"""You are ArchitectAgent 🏗️, a system architect and technical planner.

TASK: {state['current_task']}

MODE: {self.mode} (architecture & planning)
ITERATION: {state['iteration'] + 1}/{state['max_iterations']}

CONSTRAINTS:
- You can READ any file
- You can WRITE only documentation: {allowed_docs}
- You CANNOT execute code or commands
- Focus on design, specs, documentation

MEMORY:
{memory_str or "No similar architecture experiences."}

PREVIOUS ACTIONS:
{previous_actions}

AVAILABLE TOOLS:
- read_file: Read any file
- search_files: Find files
- list_files: List directory contents
- codebase_search: Search in code
- write_to_file: Write documentation (only {allowed_docs})
- update_file: Update documentation
- plan_task: Create execution plan

As ArchitectAgent, focus on:
1. Analyzing system structure
2. Documenting architecture decisions
3. Creating technical specs
4. Planning migrations and designs
5. Writing README, ARCHITECTURE.md, etc.

SYSTEM STATUS:
{system_status_str or "No system status info available."}

REASONING: <your architectural analysis>
ACTION: <tool_name>
ARGS: <json dict>

Your response:"""

        response = self.llm.invoke(prompt)
        state["reasoning_chain"].append(response)
        state["messages"].append(f"[THINK-ARCHITECT] {response[:500]}...")

        return state


__all__ = ["ArchitectAgent"]
