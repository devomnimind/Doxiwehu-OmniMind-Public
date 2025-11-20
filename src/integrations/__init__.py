"""Integration helpers for external services and protocols.

This module provides integrations for:
- Model Context Protocol (MCP) client and server
- D-Bus system integration
- OAuth 2.0 authentication
- Webhook framework
- GraphQL and Supabase
"""

from .dbus_controller import DBusSessionController, DBusSystemController
from .mcp_client import MCPClient, MCPClientError
from .mcp_client_enhanced import EnhancedMCPClient, CircuitBreaker, CircuitOpenError
from .graphql_supabase import GraphQLSupabaseHelper, GraphQLSupabaseError
from .mcp_server import MCPConfig, MCPRequestError, MCPServer
from .oauth2_client import OAuth2Client, OAuth2Config, OAuth2Token, OAuth2Error
from .webhook_framework import (
    WebhookReceiver,
    WebhookSender,
    WebhookEvent,
    WebhookConfig,
    WebhookError,
)

__all__ = [
    # MCP
    "MCPConfig",
    "MCPRequestError",
    "MCPServer",
    "MCPClient",
    "MCPClientError",
    "EnhancedMCPClient",
    "CircuitBreaker",
    "CircuitOpenError",
    # D-Bus
    "DBusSessionController",
    "DBusSystemController",
    # OAuth
    "OAuth2Client",
    "OAuth2Config",
    "OAuth2Token",
    "OAuth2Error",
    # Webhooks
    "WebhookReceiver",
    "WebhookSender",
    "WebhookEvent",
    "WebhookConfig",
    "WebhookError",
    # GraphQL/Supabase
    "GraphQLSupabaseHelper",
    "GraphQLSupabaseError",
]
