#!/usr/bin/env python3
"""
ArchitectAgent - Agente de planejamento e arquitetura
Modo: architect (🏗️)

Função: Planejar, documentar e decidir sobre arquitetura de sistema
Restrição: Edita APENAS arquivos .md, .yaml, .json (documentação)
Ferramentas: read, edit (restrito), search

Quando usar: Criar plano de migração, fazer diagrama, documentar APIs
Integração: Suporta code/debug; recebe delegação do Orchestrator
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

from .react_agent import ReactAgent, AgentState
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

    def __init__(self, config_path: str):
        super().__init__(config_path)

        self.tools_framework = ToolsFramework()
        self.mode = "architect"

        # Extensões permitidas para escrita
        self.writable_extensions = [".md", ".yaml", ".yml", ".json", ".txt", ".rst"]

        # Categorias permitidas
        self.allowed_tool_categories = [
            ToolCategory.PERCEPTION,  # Ler tudo
            ToolCategory.ORCHESTRATION,  # Planejar
        ]

    def _validate_write_permission(self, filepath: str) -> bool:
        """Valida se pode escrever em arquivo (só documentação)"""
        ext = Path(filepath).suffix.lower()
        return ext in self.writable_extensions

    def _execute_action(self, action: str, args: dict) -> str:
        """Executa ação com restrições de arquitetura"""
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
                    return f"ArchitectAgent can only edit documentation files ({', '.join(self.writable_extensions)}). Cannot edit: {filepath}"

            # Bloquear execução de comandos
            if action == "execute_command":
                return "ArchitectAgent cannot execute commands. Delegate to CodeAgent or DebugAgent."

            # Verificar ferramenta existe
            if action not in self.tools_framework.tools:
                return f"Unknown tool: {action}"

            # Verificar categoria
            tool = self.tools_framework.tools[action]
            if tool.category not in self.allowed_tool_categories:
                return f"Tool '{action}' not allowed in architect mode"

            # Executar
            result = self.tools_framework.execute_tool(action, **args)

            if isinstance(result, (dict, list)):
                return json.dumps(result, indent=2)
            return str(result)

        except Exception as e:
            return f"Error: {str(e)}"

    def _think_node(self, state: AgentState) -> AgentState:
        """THINK específico para arquitetura"""
        similar_episodes = self.memory.search_similar(state["current_task"], top_k=3)
        system_status = self.tools_framework.execute_tool("inspect_context")

        memory_str = ""
        if similar_episodes:
            memory_str = "\n".join(
                [
                    f"{i+1}. {ep['task']} → {ep['result'][:100]}"
                    for i, ep in enumerate(similar_episodes)
                ]
            )

        prompt = f"""You are ArchitectAgent 🏗️, a system architect and technical planner.

TASK: {state['current_task']}

MODE: {self.mode} (architecture & planning)
ITERATION: {state['iteration'] + 1}/{state['max_iterations']}

CONSTRAINTS:
- You can READ any file
- You can WRITE only documentation: {', '.join(self.writable_extensions)}
- You CANNOT execute code or commands
- Focus on design, specs, documentation

MEMORY:
{memory_str or "No similar architecture experiences."}

PREVIOUS ACTIONS:
{chr(10).join([f"- {a['action']}({a.get('args', {})})" for a in state['actions_taken']]) if state['actions_taken'] else "None"}

AVAILABLE TOOLS:
- read_file: Read any file
- search_files: Find files
- list_files: List directory contents
- codebase_search: Search in code
- write_to_file: Write documentation (only {', '.join(self.writable_extensions)})
- update_file: Update documentation
- plan_task: Create execution plan

As ArchitectAgent, focus on:
1. Analyzing system structure
2. Documenting architecture decisions
3. Creating technical specs
4. Planning migrations and designs
5. Writing README, ARCHITECTURE.md, etc.

REASONING: <your architectural analysis>
ACTION: <tool_name>
ARGS: <json dict>

Your response:"""

        response = self.llm.invoke(prompt)
        state["reasoning_chain"].append(response)
        state["messages"].append(f"[THINK-ARCHITECT] {response[:500]}...")

        return state


__all__ = ["ArchitectAgent"]
