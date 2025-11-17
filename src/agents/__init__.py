"""
OmniMind Agents - Multi-Agent System with Specialized Roles

Agents:
- ReactAgent: Base agent with Think→Act→Observe loop
- CodeAgent (💻): Code development specialist
- ArchitectAgent (🏗️): Architecture & planning specialist
- DebugAgent (🪲): Debugging & diagnosis specialist
- ReviewerAgent (⭐): Code review with RLAIF scoring
- OrchestratorAgent (🪃): Master coordinator

Usage:
    from src.agents import OrchestratorAgent

    orchestrator = OrchestratorAgent("config/agent_config.yaml")
    result = orchestrator.run_orchestrated_task("Build authentication system")
"""

from .react_agent import ReactAgent, AgentState
from .code_agent import CodeAgent
from .architect_agent import ArchitectAgent
from .debug_agent import DebugAgent
from .reviewer_agent import ReviewerAgent
from .orchestrator_agent import OrchestratorAgent, AgentMode

__all__ = [
    "ReactAgent",
    "AgentState",
    "CodeAgent",
    "ArchitectAgent",
    "DebugAgent",
    "ReviewerAgent",
    "OrchestratorAgent",
    "AgentMode",
]
