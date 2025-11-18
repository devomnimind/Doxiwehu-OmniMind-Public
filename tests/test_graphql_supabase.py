from __future__ import annotations

from typing import Any, Optional

import pytest

from src.integrations.graphql_supabase import (
    GraphQLCollectionPage,
    GraphQLSupabaseError,
    GraphQLSupabaseHelper,
)
from src.integrations.supabase_adapter import SupabaseConfig


class DummyResponse:
    def __init__(self, status_code: int, payload: Any):
        self.status_code = status_code
        self._payload = payload

    def json(self) -> Any:
        return self._payload


class DummySession:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []
        self.next_response: Optional[DummyResponse] = None

    def post(self, url: str, json: dict[str, Any], headers: dict[str, str], timeout: float) -> DummyResponse:
        self.calls.append((url, json))
        if self.next_response:
            response = self.next_response
            self.next_response = None
            return response
        return DummyResponse(200, {"data": {
            "memory_consolidations": {
                "edges": [
                    {"node": {"id": "1", "payload": "a"}},
                ],
                "pageInfo": {
                    "hasNextPage": False,
                    "endCursor": "cur"
                },
            }
        }})


@pytest.fixture
def config(tmp_path) -> SupabaseConfig:
    return SupabaseConfig(url="https://supabase.test", anon_key="anon", service_role_key="service")


@pytest.fixture
def helper(config: SupabaseConfig) -> GraphQLSupabaseHelper:
    return GraphQLSupabaseHelper(config=config, session=DummySession())


def test_fetch_page(helper: GraphQLSupabaseHelper):
    page = helper.fetch_page("memory_consolidations", ["id", "payload"], first=1)
    assert isinstance(page, GraphQLCollectionPage)
    assert page.nodes == [{"id": "1", "payload": "a"}]
    assert page.has_next is False
    assert page.cursor == "cur"


def test_empty_collection(helper: GraphQLSupabaseHelper):
    helper.session.next_response = DummyResponse(200, {"data": {}})
    with pytest.raises(GraphQLSupabaseError):
        helper.fetch_page("memory_consolidations", ["id"], first=1)


def test_graphql_error(helper: GraphQLSupabaseHelper):
    helper.session.next_response = DummyResponse(200, {"data": None, "errors": [{"message": "boom"}]})
    with pytest.raises(GraphQLSupabaseError):
        helper.fetch_page("memory_consolidations", ["id"], first=1)


def test_iterate_collection(helper: GraphQLSupabaseHelper):
    nodes = list(helper.iterate_collection("memory_consolidations", ["id"], page_size=1, max_pages=1))
    assert nodes == [{"id": "1", "payload": "a"}]


def test_collect_nodes(helper: GraphQLSupabaseHelper):
    nodes = helper.collect_nodes("memory_consolidations", ["id", "payload"], page_size=1)
    assert nodes[0]["payload"] == "a"
