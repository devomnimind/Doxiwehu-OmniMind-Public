"""
Orchestrator module - Componentes centrais de orquestração do OmniMind.

Implementa recomendações da AUDITORIA_ORCHESTRATOR_COMPLETA.md:
- AgentRegistry: Registro centralizado de agentes com health checks
- EventBus: Sistema de eventos priorizado
- CircuitBreaker: Proteção contra cascata de falhas
"""

from .agent_registry import AgentPriority, AgentRegistry
from .circuit_breaker import AgentCircuitBreaker, CircuitBreakerOpen, CircuitState
from .event_bus import EventPriority, OrchestratorEvent, OrchestratorEventBus

__all__ = [
    "AgentRegistry",
    "AgentPriority",
    "OrchestratorEventBus",
    "EventPriority",
    "OrchestratorEvent",
    "AgentCircuitBreaker",
    "CircuitBreakerOpen",
    "CircuitState",
]
