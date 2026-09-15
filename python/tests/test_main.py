"""Tests for CLI arg parsing and transport selection — mirrors modelcontextprotocol/src/test/main.test.ts."""
import pytest
from unittest.mock import patch, MagicMock, call

from commerce_mcp.config import ClientCredentialsAuth, ExistingTokenAuth, CTContext


def _set_base_env(monkeypatch):
    monkeypatch.setenv("AUTH_URL", "https://auth.commercetools.com")
    monkeypatch.setenv("API_URL", "https://api.commercetools.com")
    monkeypatch.setenv("PROJECT_KEY", "test-project")
    monkeypatch.setenv("CLIENT_ID", "test-id")
    monkeypatch.setenv("CLIENT_SECRET", "test-secret")


# ── _parse_tools ──────────────────────────────────────────────────────────────

def test_parse_tools_all_returns_none():
    from commerce_mcp.__main__ import _parse_tools
    assert _parse_tools("all") is None


def test_parse_tools_all_read_enables_read_on_all():
    from commerce_mcp.__main__ import _parse_tools
    actions = _parse_tools("all.read")
    assert actions.products.read is True
    assert actions.products.create is False


def test_parse_tools_specific_namespace_and_permission():
    from commerce_mcp.__main__ import _parse_tools
    actions = _parse_tools("products.read")
    assert actions.products.read is True
    assert actions.order is None


def test_parse_tools_multiple():
    from commerce_mcp.__main__ import _parse_tools
    actions = _parse_tools("products.read,order.create")
    assert actions.products.read is True
    assert actions.order.create is True


def test_parse_tools_combines_permissions_for_same_namespace():
    from commerce_mcp.__main__ import _parse_tools
    actions = _parse_tools("products.read,products.create")
    assert actions.products.read is True
    assert actions.products.create is True


# ── _build_auth ───────────────────────────────────────────────────────────────

def test_build_auth_uses_client_credentials(monkeypatch):
    _set_base_env(monkeypatch)
    from commerce_mcp.__main__ import _build_auth
    auth = _build_auth()
    assert isinstance(auth, ClientCredentialsAuth)
    assert auth.client_id == "test-id"


def test_build_auth_prefers_access_token(monkeypatch):
    _set_base_env(monkeypatch)
    monkeypatch.setenv("ACCESS_TOKEN", "bearer-token-123")
    from commerce_mcp.__main__ import _build_auth
    auth = _build_auth()
    assert isinstance(auth, ExistingTokenAuth)
    assert auth.access_token == "bearer-token-123"


def test_build_auth_exits_when_no_credentials(monkeypatch):
    monkeypatch.setenv("AUTH_URL", "https://auth.commercetools.com")
    monkeypatch.setenv("API_URL", "https://api.commercetools.com")
    monkeypatch.setenv("PROJECT_KEY", "test-project")
    monkeypatch.delenv("CLIENT_ID", raising=False)
    monkeypatch.delenv("CLIENT_SECRET", raising=False)
    monkeypatch.delenv("ACCESS_TOKEN", raising=False)
    with pytest.raises(SystemExit):
        from commerce_mcp.__main__ import _build_auth
        _build_auth()


# ── main() transport dispatch ─────────────────────────────────────────────────

def test_main_stdio_transport(monkeypatch):
    _set_base_env(monkeypatch)
    monkeypatch.setenv("TOOLS", "all")

    mock_server = MagicMock()
    with patch("commerce_mcp.__main__.build_server", return_value=mock_server):
        from commerce_mcp.__main__ import main
        main(["--transport", "stdio", "--tools", "all"])
        mock_server.run.assert_called_once_with(transport="stdio")


def test_main_http_transport(monkeypatch):
    _set_base_env(monkeypatch)

    mock_server = MagicMock()
    with patch("commerce_mcp.__main__.build_server", return_value=mock_server):
        from commerce_mcp.__main__ import main
        main(["--transport", "http", "--port", "9000", "--tools", "all"])
        mock_server.run.assert_called_once_with(
            transport="streamable-http",
            host="0.0.0.0",
            port=9000,
        )


def test_main_sets_admin_context_from_env(monkeypatch):
    _set_base_env(monkeypatch)
    monkeypatch.setenv("IS_ADMIN", "true")

    captured = {}
    def _fake_build(auth, config):
        captured["config"] = config
        return MagicMock()

    with patch("commerce_mcp.__main__.build_server", side_effect=_fake_build):
        from commerce_mcp.__main__ import main
        main(["--transport", "stdio"])
        assert captured["config"].context.is_admin is True


def test_main_sets_customer_context_from_env(monkeypatch):
    _set_base_env(monkeypatch)
    monkeypatch.setenv("CUSTOMER_ID", "cust-999")

    captured = {}
    def _fake_build(auth, config):
        captured["config"] = config
        return MagicMock()

    with patch("commerce_mcp.__main__.build_server", side_effect=_fake_build):
        from commerce_mcp.__main__ import main
        main(["--transport", "stdio"])
        assert captured["config"].context.customer_id == "cust-999"


# ── Integration adapters (smoke tests) ────────────────────────────────────────

def test_get_ai_sdk_tools_returns_openai_format():
    from commerce_mcp.config import Configuration, Actions, ResourceActions
    from commerce_mcp.integrations.ai_sdk import get_ai_sdk_tools
    config = Configuration(actions=Actions(products=ResourceActions(read=True)))
    tools = get_ai_sdk_tools(config)
    assert len(tools) > 0
    tool = tools[0]
    assert tool["type"] == "function"
    assert "name" in tool["function"]
    assert "parameters" in tool["function"]


def test_get_anthropic_tools_returns_anthropic_format():
    from commerce_mcp.config import Configuration, Actions, ResourceActions
    from commerce_mcp.integrations.anthropic_sdk import get_anthropic_tools
    config = Configuration(actions=Actions(products=ResourceActions(read=True)))
    tools = get_anthropic_tools(config)
    assert len(tools) > 0
    tool = tools[0]
    assert "name" in tool
    assert "description" in tool
    assert "input_schema" in tool
