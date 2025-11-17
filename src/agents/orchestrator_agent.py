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

import json
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime

from .react_agent import ReactAgent, AgentState
from .code_agent import CodeAgent
from .architect_agent import ArchitectAgent
from .debug_agent import DebugAgent
from .reviewer_agent import ReviewerAgent
from ..tools.omnimind_tools import ToolsFramework, ToolCategory


class AgentMode(Enum):
    """Modos de agente disponíveis"""

    ORCHESTRATOR = "orchestrator"
    CODE = "code"
    ARCHITECT = "architect"
    DEBUG = "debug"
    REVIEWER = "reviewer"
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

    def __init__(self, config_path: str):
        super().__init__(config_path)

        self.tools_framework = ToolsFramework()
        self.mode = "orchestrator"

        # Agentes especializados (lazy init)
        self._agents: Dict[AgentMode, ReactAgent] = {}
        self.config_path = config_path

        # Estado de orquestração
        self.current_plan = None
        self.delegated_tasks = []
        self.completed_subtasks = []

    def _timestamp(self) -> str:
        """Retorna timestamp UTC em formato ISO"""
        return datetime.utcnow().isoformat() + "Z"

    def _get_agent(self, mode: AgentMode) -> ReactAgent:
        """Obtém ou cria agente especializado"""
        if mode not in self._agents:
            if mode == AgentMode.CODE:
                self._agents[mode] = CodeAgent(self.config_path)
            elif mode == AgentMode.ARCHITECT:
                self._agents[mode] = ArchitectAgent(self.config_path)
            elif mode == AgentMode.DEBUG:
                self._agents[mode] = DebugAgent(self.config_path)
            elif mode == AgentMode.REVIEWER:
                self._agents[mode] = ReviewerAgent(self.config_path)
            else:
                raise ValueError(f"Unknown agent mode: {mode}")

        return self._agents[mode]

    def decompose_task(self, task_description: str) -> Dict[str, Any]:
        """Decompõe tarefa complexa em subtarefas delegáveis"""
        prompt = f"""You are OrchestratorAgent 🪃, a master coordinator of specialist agents.

COMPLEX TASK: {task_description}

AVAILABLE SPECIALIST AGENTS:
- CodeAgent (code): Implements features, writes code, runs tests
- ArchitectAgent (architect): Plans architecture, writes specs/docs
- DebugAgent (debug): Diagnoses bugs, analyzes errors
- ReviewerAgent (reviewer): Reviews quality, provides RLAIF feedback

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

        response = self.llm.invoke(prompt)

        # Parsear plano
        plan = self._parse_plan(response)
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

        in_subtasks = False
        for line in response.split("\n"):
            line = line.strip()

            if "SUBTASKS:" in line:
                in_subtasks = True
                continue

            if "DEPENDENCIES:" in line:
                in_subtasks = False
                continue

            if in_subtasks and line and (line[0].isdigit() or line.startswith("-")):
                # Extrair modo e descrição - flexível para [CODE], [CODE_MODE], (code), etc.
                line_lower = line.lower()
                matched = False
                for mode in ["code", "architect", "debug", "reviewer"]:
                    # Buscar variações: [code], [code_mode], (code), etc.
                    if (
                        f"[{mode}]" in line_lower
                        or f"[{mode}_mode]" in line_lower
                        or f"({mode})" in line_lower
                        or f"{mode}_mode" in line_lower
                    ):
                        # Extrair descrição após modo
                        task_desc = (
                            line.split("]", 1)[-1].strip() if "]" in line else line
                        )
                        # Remover padrões como "- Plan Architecture:"
                        if ":" in task_desc:
                            task_desc = task_desc.split(":", 1)[-1].strip()
                        plan["subtasks"].append(
                            {
                                "agent": mode,
                                "description": task_desc,
                                "status": "pending",
                            }
                        )
                        matched = True
                        break

                # Se não encontrou modo explícito, tentar inferir
                if not matched:
                    for mode in ["code", "architect", "debug", "reviewer"]:
                        agent_names = {
                            "code": [
                                "codeagent",
                                "code agent",
                                "implement",
                                "write code",
                            ],
                            "architect": [
                                "architectagent",
                                "architect agent",
                                "plan",
                                "design",
                                "specification",
                            ],
                            "debug": [
                                "debugagent",
                                "debug agent",
                                "diagnose",
                                "fix bug",
                            ],
                            "reviewer": [
                                "revieweragent",
                                "reviewer agent",
                                "review",
                                "quality",
                            ],
                        }
                        if any(keyword in line_lower for keyword in agent_names[mode]):
                            task_desc = line.strip("0123456789.-) \t")
                            if ":" in task_desc:
                                task_desc = task_desc.split(":", 1)[-1].strip()
                            plan["subtasks"].append(
                                {
                                    "agent": mode,
                                    "description": task_desc,
                                    "status": "pending",
                                }
                            )
                            break

            if "ESTIMATED_COMPLEXITY:" in line or "complexity:" in line.lower():
                if "low" in line.lower():
                    plan["complexity"] = "low"
                elif "high" in line.lower():
                    plan["complexity"] = "high"

        return plan

    def execute_plan(
        self, plan: Dict[str, Any] = None, max_iterations_per_task: int = 3
    ) -> Dict[str, Any]:
        """Executa plano delegando para agentes especializados"""
        if plan is None:
            plan = self.current_plan

        if not plan or not plan.get("subtasks"):
            return {"error": "No plan to execute"}

        results = {
            "original_task": plan.get("original_task"),
            "subtask_results": [],
            "overall_success": True,
            "started_at": self._timestamp(),
        }

        for i, subtask in enumerate(plan["subtasks"]):
            print(
                f"\n🪃 [Orchestrator] Delegating subtask {i+1}/{len(plan['subtasks'])}: {subtask['description'][:80]}..."
            )

            try:
                # Determinar agente
                agent_mode = AgentMode(subtask["agent"])
                agent = self._get_agent(agent_mode)

                # Criar tarefa via ToolsFramework
                task_record = self.tools_framework.execute_tool(
                    "new_task",
                    task_name=subtask["description"],
                    assigned_to=subtask["agent"],
                    priority="HIGH" if plan["complexity"] == "high" else "MEDIUM",
                )

                # Trocar modo
                self.tools_framework.execute_tool(
                    "switch_mode", target_mode=subtask["agent"], reason=f"Subtask {i+1}"
                )

                # Executar subtarefa
                if agent_mode == AgentMode.CODE:
                    result = agent.run_code_task(
                        subtask["description"], max_iterations=max_iterations_per_task
                    )
                elif agent_mode == AgentMode.REVIEWER:
                    # Reviewer precisa de filepath (simplificado)
                    result = {
                        "completed": True,
                        "mode": "reviewer",
                        "note": "Review would be performed on generated files",
                    }
                else:
                    result = agent.run(
                        subtask["description"], max_iterations=max_iterations_per_task
                    )

                # Registrar resultado
                subtask["status"] = "completed" if result.get("completed") else "failed"
                subtask["result"] = result

                results["subtask_results"].append(
                    {
                        "subtask_id": i + 1,
                        "agent": subtask["agent"],
                        "description": subtask["description"],
                        "completed": result.get("completed", False),
                        "iterations": result.get("iteration", 0),
                        "summary": result.get("final_result", "")[:200],
                    }
                )

                if not result.get("completed"):
                    results["overall_success"] = False
                    print(f"❌ Subtask {i+1} failed")
                else:
                    print(f"✅ Subtask {i+1} completed")

                # Armazenar conclusão
                self.tools_framework.execute_tool(
                    "attempt_completion",
                    task_id=task_record["id"],
                    result=str(result.get("final_result", "")),
                    success=result.get("completed", False),
                )

            except Exception as e:
                print(f"❌ Error in subtask {i+1}: {e}")
                results["overall_success"] = False
                results["subtask_results"].append(
                    {"subtask_id": i + 1, "error": str(e)}
                )

        results["completed_at"] = self._timestamp()

        # Voltar para modo orchestrator
        self.tools_framework.execute_tool(
            "switch_mode", target_mode="orchestrator", reason="Plan execution complete"
        )

        return results

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

        # 1. Decompor
        print("📋 Decomposing task into subtasks...")
        plan = self.decompose_task(task)

        print(f"\n📊 Plan created with {len(plan['subtasks'])} subtasks:")
        for i, subtask in enumerate(plan["subtasks"], 1):
            print(f"  {i}. [{subtask['agent']}] {subtask['description'][:80]}")

        # 2. Executar
        print(f"\n🚀 Executing plan...")
        execution_result = self.execute_plan(plan, max_iterations_per_subtask)

        # 3. Sintetizar
        print(f"\n📝 Synthesizing results...")
        synthesis = self._synthesize_results(execution_result)

        # 4. Armazenar episódio completo
        self.memory.store_episode(
            task=task,
            action=f"Orchestrated {len(plan['subtasks'])} subtasks",
            result=synthesis["summary"],
            reward=1.0 if execution_result["overall_success"] else 0.5,
        )

        return {
            "task": task,
            "plan": plan,
            "execution": execution_result,
            "synthesis": synthesis,
            "success": execution_result["overall_success"],
        }

    def _synthesize_results(self, execution_result: Dict) -> Dict[str, Any]:
        """Sintetiza resultados de múltiplos agentes"""
        subtask_summaries = []
        for sr in execution_result["subtask_results"]:
            subtask_summaries.append(
                f"- {sr.get('agent', 'unknown')}: {sr.get('description', '')} → "
                f"{'✅' if sr.get('completed') else '❌'}"
            )

        synthesis = {
            "summary": "\n".join(subtask_summaries),
            "total_subtasks": len(execution_result["subtask_results"]),
            "completed": sum(
                1 for sr in execution_result["subtask_results"] if sr.get("completed")
            ),
            "failed": sum(
                1
                for sr in execution_result["subtask_results"]
                if not sr.get("completed")
            ),
            "overall_success": execution_result["overall_success"],
        }

        return synthesis


# ============================================================================
# EXPORTAÇÕES
# ============================================================================

__all__ = ["OrchestratorAgent", "AgentMode"]
