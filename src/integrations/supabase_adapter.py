from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    from supabase import Client, create_client
except ImportError as exc:
    Client = Any  # type: ignore[assignment]

    def create_client(*args: Any, **kwargs: Any) -> Any:
        raise ImportError("Install supabase-py to use SupabaseAdapter") from exc

from .mcp_client import MCPClient, MCPClientError

logger = logging.getLogger(__name__)


class SupabaseAdapterError(Exception):
    pass


@dataclass(frozen=True)
class SupabaseConfig:
    url: str
    anon_key: str
    service_role_key: Optional[str] = None
    project_ref: Optional[str] = None

    @property
    def has_service_role_key(self) -> bool:
        return bool(self.service_role_key)

    @classmethod
    def from_env(cls) -> Optional["SupabaseConfig"]:
        url = os.environ.get("OMNIMIND_SUPABASE_URL")
        anon_key = os.environ.get("OMNIMIND_SUPABASE_ANON_KEY")
        if not url or not anon_key:
            return None
        return cls(
            url=url,
            anon_key=anon_key,
            service_role_key=os.environ.get("OMNIMIND_SUPABASE_SERVICE_ROLE_KEY"),
            project_ref=os.environ.get("OMNIMIND_SUPABASE_PROJECT"),
        )

    @classmethod
    def from_text(cls, text: str) -> Optional["SupabaseConfig"]:
        matches: Dict[str, str] = {}
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = map(str.strip, line.split("=", 1))
            clean_value = value.strip().strip("\"' ")
            matches[key] = clean_value
        url = matches.get("NEXT_PUBLIC_SUPABASE_URL")
        anon_key = matches.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
        if not url or not anon_key:
            return None
        service_key = matches.get("OMNIMIND_SUPABASE_SERVICE_ROLE_KEY")
        if not service_key:
            service_key = matches.get("SERVICE ROLE KEY")
        if not service_key:
            service_key = matches.get("SERVICE_ROLE_KEY")
        project_ref = matches.get("OMNIMIND_SUPABASE_PROJECT")
        return cls(url=url, anon_key=anon_key, service_role_key=service_key, project_ref=project_ref)

    @classmethod
    def load(cls, mcp_client: Optional[MCPClient] = None) -> Optional["SupabaseConfig"]:
        servers_path = Path("docs/servers.txt")
        if mcp_client is not None:
            try:
                data = mcp_client.read_file(str(servers_path))
            except MCPClientError as exc:
                logger.debug("Unable to read servers via MCP: %s", exc)
            else:
                config = cls.from_text(data)
                if config:
                    return config
        if servers_path.exists():
            config = cls.from_text(servers_path.read_text(encoding="utf-8"))
            if config:
                return config
        return cls.from_env()


class SupabaseAdapter:
    def __init__(self, config: SupabaseConfig):
        self.config = config
        self.client: Client = create_client(config.url, config.anon_key)
        self.admin_client: Optional[Client] = (
            create_client(config.url, config.service_role_key)
            if config.service_role_key
            else None
        )

    def describe_table(self, table: str) -> List[Dict[str, Any]]:
        if not self.admin_client:
            raise SupabaseAdapterError("Service role key required to describe schema")
        orm = self.admin_client.table("information_schema.columns")
        query = (
            orm.select("column_name, data_type, is_nullable, column_default")
            .eq("table_name", table)
            .eq("table_schema", "public")
        )
        response = query.execute()
        if response.error:
            raise SupabaseAdapterError(response.error)
        return response.data

    def list_tables(self) -> List[str]:
        if not self.admin_client:
            raise SupabaseAdapterError("Service role key required to enumerate tables")
        response = (
            self.admin_client.table("information_schema.tables")
            .select("table_name, table_type")
            .eq("table_schema", "public")
            .execute()
        )
        if response.error:
            raise SupabaseAdapterError(response.error)
        return [row.get("table_name") for row in response.data if row]

    def query_table(
        self,
        table: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20,
        offset: int = 0,
        columns: Optional[Iterable[str]] = None,
    ) -> List[Dict[str, Any]]:
        query = self.client.table(table).select("*" if not columns else ",".join(columns))
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        response = query.limit(limit).offset(offset).execute()
        if response.error:
            raise SupabaseAdapterError(response.error)
        return response.data

    def insert_record(self, table: str, record: Dict[str, Any]) -> Dict[str, Any]:
        response = self.client.table(table).insert(record).execute()
        if response.error:
            raise SupabaseAdapterError(response.error)
        return response.data

    def update_record(self, table: str, record: Dict[str, Any], match: Dict[str, Any]) -> Dict[str, Any]:
        query = self.client.table(table)
        for key, value in match.items():
            query = query.eq(key, value)
        response = query.update(record).execute()
        if response.error:
            raise SupabaseAdapterError(response.error)
        return response.data

    def delete_records(self, table: str, match: Dict[str, Any]) -> Dict[str, Any]:
        query = self.client.table(table)
        for key, value in match.items():
            query = query.eq(key, value)
        response = query.delete().execute()
        if response.error:
            raise SupabaseAdapterError(response.error)
        return response.data

    def log_operation(self, name: str, status: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        payload = {
            "name": name,
            "status": status,
            "source": "SupabaseAdapter",
            "timestamp": os.environ.get("OMNIMIND_TIMESTAMP") or "",
        }
        if metadata:
            payload["metadata"] = metadata
        logger.info("Supabase operation %s", payload)