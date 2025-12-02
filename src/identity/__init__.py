"""
Agent Identity and Digital Signature Module

This module implements digital identity and reputation systems for autonomous agents,
allowing them to sign their work, build reputation, and maintain verifiable identity.
"""

from .agent_signature import (
    SymbolicAuthority,
    AuthorityState,
    AgentIdentity,
)

__all__ = [
    "SymbolicAuthority",
    "AuthorityState",
    "AgentIdentity",
]
