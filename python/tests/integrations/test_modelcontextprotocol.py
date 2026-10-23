"""Tests for FastMCP server construction — mirrors modelcontextprotocol/src/test/."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from commerce_mcp.config import (
    ClientCredentialsAuth,
    Configuration,
    CTContext,
    Actions,
    ResourceActions,
)
from commerce_mcp.server import build_server, make_lifespan


@pytest.fixture
def auth(client_credentials_auth):
    return client_credentials_auth


def _tool_names(server) -> list[str]:
    """Extract registered tool names from a FastMCP server."""
    import asyncio
    tools = asyncio.run(server.list_tools())
    return [t.name for t in tools]


# ── Tool registration ──────────────────────────────────────────────────────────

def test_build_server_registers_products_tools_when_allowed(auth):
    config = Configuration(actions=Actions(products=ResourceActions(read=True)))
    server = build_server(auth, config)
    names = _tool_names(server)
    assert "list_products" in names


def test_build_server_excludes_create_when_not_permitted(auth):
    config = Configuration(actions=Actions(products=ResourceActions(read=True)))
    server = build_server(auth, config)
    names = _tool_names(server)
    assert "create_product" not in names


def test_build_server_registers_all_product_tools_when_fully_permitted(auth):
    config = Configuration(
        actions=Actions(products=ResourceActions(read=True, create=True, update=True))
    )
    server = build_server(auth, config)
    names = _tool_names(server)
    assert {"list_products", "create_product", "update_product"}.issubset(set(names))


def test_build_server_excludes_unset_namespace(auth):
    config = Configuration(actions=Actions(products=ResourceActions(read=True)))
    server = build_server(auth, config)
    names = _tool_names(server)
    assert "read_order" not in names


def test_build_server_uses_dynamic_mode_above_threshold(auth):
    config = Configuration(
        actions=Actions(
            products=ResourceActions(read=True, create=True, update=True),
            order=ResourceActions(read=True, create=True, update=True),
            cart=ResourceActions(read=True, create=True, update=True),
        ),
        context=CTContext(dynamic_tool_loading_threshold=1),
    )
    server = build_server(auth, config)
    names = _tool_names(server)
    assert "list_available_tools" in names
    assert "inject_tools" in names
    assert "execute_tool" in names
    assert "list_products" not in names


def test_build_server_unrestricted_with_no_actions(auth):
    config = Configuration()  # actions=None → all tools
    server = build_server(auth, config)
    names = _tool_names(server)
    assert len(names) > 0


# ── Lifespan ───────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_lifespan_creates_and_closes_api(auth, admin_config):
    from fastmcp import FastMCP

    with patch("commerce_mcp.server.CommercetoolsAPI") as MockAPI:
        instance = AsyncMock()
        MockAPI.create = AsyncMock(return_value=instance)
        instance.close = AsyncMock()

        server = FastMCP("test")
        lifespan_fn = make_lifespan(auth, admin_config)

        async with lifespan_fn(server) as state:
            MockAPI.create.assert_called_once_with(auth, admin_config.context)
            assert state.api is instance

        instance.close.assert_called_once()
