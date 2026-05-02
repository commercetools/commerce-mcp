"""Tests for carts context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.carts.functions import read_cart, create_cart, update_cart
from commerce_mcp.tools.carts.schemas import ReadCartParams, CreateCartParams, UpdateCartParams
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError, ContextError


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "cart-1"}]})
    api.post = AsyncMock(return_value={"id": "cart-1", "version": 2})
    return api


# ── Context dispatch ───────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_cart_routes_to_admin(mock_api):
    ctx = CTContext(is_admin=True)
    await read_cart(ReadCartParams(), mock_api, ctx)
    mock_api.get.assert_called_once()
    assert mock_api.get.call_args[0][0] == "/carts"


@pytest.mark.asyncio
async def test_read_cart_routes_to_customer(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await read_cart(ReadCartParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/me/carts"


@pytest.mark.asyncio
async def test_read_cart_routes_to_store(mock_api):
    ctx = CTContext(store_key="eu-store")
    await read_cart(ReadCartParams(), mock_api, ctx)
    assert "/in-store/key=eu-store/carts" == mock_api.get.call_args[0][0]


@pytest.mark.asyncio
async def test_read_cart_routes_to_associate(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    await read_cart(ReadCartParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=bu-1" in path


@pytest.mark.asyncio
async def test_create_cart_routes_to_customer(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await create_cart(CreateCartParams(currency="USD"), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/me/carts"


@pytest.mark.asyncio
async def test_create_cart_routes_to_store(mock_api):
    ctx = CTContext(store_key="eu-store")
    await create_cart(CreateCartParams(currency="EUR"), mock_api, ctx)
    assert "/in-store/key=eu-store/carts" == mock_api.post.call_args[0][0]


@pytest.mark.asyncio
async def test_update_cart_routes_to_admin(mock_api):
    ctx = CTContext(is_admin=True)
    await update_cart(UpdateCartParams(id="cart-1", version=1), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/carts/cart-1"


@pytest.mark.asyncio
async def test_update_cart_routes_to_customer(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await update_cart(UpdateCartParams(id="cart-1", version=1), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/me/carts/cart-1"


# ── Security: no fallthrough to admin — mirrors contextToCartFunctionMapping ──

@pytest.mark.asyncio
async def test_read_cart_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()  # no is_admin, no customer_id, no store_key
    with pytest.raises(ContextError, match="read_cart"):
        await read_cart(ReadCartParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


@pytest.mark.asyncio
async def test_create_cart_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_cart"):
        await create_cart(CreateCartParams(currency="USD"), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_cart_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_cart"):
        await update_cart(UpdateCartParams(id="cart-1", version=1), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── SDK errors ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_cart_raises_sdk_error_on_failure(mock_api):
    mock_api.get.side_effect = Exception("500 Server Error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to read cart"):
        await read_cart(ReadCartParams(), mock_api, ctx)
