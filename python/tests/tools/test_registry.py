"""Tests for the tool registry and permission filtering."""
import pytest
from commerce_mcp.config import Configuration, Actions, ResourceActions, CTContext
from commerce_mcp.tools.registry import get_tools, ToolDefinition


@pytest.fixture(autouse=True)
def _ensure_namespaces_imported():
    """Force namespace modules to self-register before each test."""
    from commerce_mcp.tools import products, orders, carts  # noqa: F401


def test_get_tools_returns_all_when_no_actions():
    config = Configuration()
    tools = get_tools(config)
    names = {t.method for t in tools}
    assert "list_products" in names
    assert "read_order" in names
    assert "read_cart" in names


def test_get_tools_filters_by_read_only():
    config = Configuration(
        actions=Actions(products=ResourceActions(read=True))
    )
    tools = get_tools(config)
    names = {t.method for t in tools}
    assert "list_products" in names
    assert "create_product" not in names
    assert "update_product" not in names


def test_get_tools_allows_create_when_enabled():
    config = Configuration(
        actions=Actions(products=ResourceActions(read=True, create=True))
    )
    tools = get_tools(config)
    names = {t.method for t in tools}
    assert "create_product" in names
    assert "update_product" not in names


def test_get_tools_excludes_namespace_not_in_actions():
    config = Configuration(
        actions=Actions(products=ResourceActions(read=True))
        # orders not set → excluded
    )
    tools = get_tools(config)
    names = {t.method for t in tools}
    assert "read_order" not in names


def test_tool_has_required_fields():
    config = Configuration()
    tools = get_tools(config)
    for tool in tools:
        assert tool.method, "method should not be empty"
        assert tool.name, "name should not be empty"
        assert tool.description, "description should not be empty"
        assert tool.parameters is not None
        assert callable(tool.handler)
        assert isinstance(tool.actions, dict)


@pytest.mark.parametrize("tool_name,expected_namespace", [
    ("list_products", "products"),
    ("create_product", "products"),
    ("read_order", "order"),
    ("create_order", "order"),
    ("read_cart", "cart"),
])
def test_tool_actions_have_correct_namespace(tool_name: str, expected_namespace: str):
    config = Configuration()
    registry = {t.method: t for t in get_tools(config)}
    tool = registry[tool_name]
    assert expected_namespace in tool.actions
