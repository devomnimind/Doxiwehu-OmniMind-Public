"""
Módulo de auditoria para OmniMind.
Sistema de logging imutável com chain hashing.
"""

from .immutable_audit import ImmutableAuditSystem, get_audit_system, log_action

__all__ = ["ImmutableAuditSystem", "get_audit_system", "log_action"]
