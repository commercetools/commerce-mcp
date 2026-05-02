"""Tests for orders context-conditional dispatch — mirrors typescript/src/test/shared/order/."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from commerce_mcp.tools.orders.functions import (
    read_order,
    create_order,
    update_order,
    _read_order_admin,
    _read_order_customer,
    _read_order_store,
    _read_order_as_associate,
)
from commerce_mcp.tools.orders.schemas import ReadOrderParams, CreateOrderParams, UpdateOrderParams
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError, ContextError


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "order-123"}]})
    api.post = AsyncMock(return_value={"id": "order-123", "version": 2})
    return api


# ── Context-conditional dispatch ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_order_dispatches_to_admin(mock_api):
    ctx = CTContext(is_admin=True)
    with patch(
        "commerce_mcp.tools.orders.functions._read_order_admin",
        new=AsyncMock(return_value="admin result"),
    ) as mock_fn:
        await read_order(ReadOrderParams(), mock_api, ctx)
        mock_fn.assert_called_once()


@pytest.mark.asyncio
async def test_read_order_dispatches_to_customer(mock_api):
    ctx = CTContext(customer_id="cust-1")
    with patch(
        "commerce_mcp.tools.orders.functions._read_order_customer",
        new=AsyncMock(return_value="customer result"),
    ) as mock_fn:
        await read_order(ReadOrderParams(), mock_api, ctx)
        mock_fn.assert_called_once()


@pytest.mark.asyncio
async def test_read_order_dispatches_to_store(mock_api):
    ctx = CTContext(store_key="my-store")
    with patch(
        "commerce_mcp.tools.orders.functions._read_order_store",
        new=AsyncMock(return_value="store result"),
    ) as mock_fn:
        await read_order(ReadOrderParams(), mock_api, ctx)
        mock_fn.assert_called_once()


@pytest.mark.asyncio
async def test_read_order_dispatches_to_associate_when_both_set(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-key")
    with patch(
        "commerce_mcp.tools.orders.functions._read_order_as_associate",
        new=AsyncMock(return_value="associate result"),
    ) as mock_fn:
        await read_order(ReadOrderParams(), mock_api, ctx)
        mock_fn.assert_called_once()


# ── Implementation details ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_order_admin_uses_orders_endpoint(mock_api):
    ctx = CTContext(is_admin=True)
    await _read_order_admin(ReadOrderParams(limit=5), mock_api, ctx)
    mock_api.get.assert_called_once_with("/orders", params={"limit": 5})


@pytest.mark.asyncio
async def test_read_order_customer_filters_by_customer_id(mock_api):
    ctx = CTContext(customer_id="cust-42")
    await _read_order_customer(ReadOrderParams(), mock_api, ctx)
    params = mock_api.get.call_args[1]["params"]
    assert "cust-42" in params.get("where", "")


@pytest.mark.asyncio
async def test_read_order_store_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await _read_order_store(ReadOrderParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=eu-store/orders" == path


@pytest.mark.asyncio
async def test_read_order_associate_uses_as_associate_path(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="my-bu")
    await _read_order_as_associate(ReadOrderParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=my-bu" in path


@pytest.mark.asyncio
async def test_read_order_raises_sdk_error(mock_api):
    mock_api.get.side_effect = Exception("Network error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to read order"):
        await _read_order_admin(ReadOrderParams(), mock_api, ctx)


# ── Security: no fallthrough to admin when context is missing ─────────────────

@pytest.mark.asyncio
async def test_read_order_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()  # no is_admin, no customer_id, no store_key
    with pytest.raises(ContextError, match="read_order"):
        await read_order(ReadOrderParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_order_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_order"):
        await create_order(CreateOrderParams(cart_id="cart-1", version=1), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_order_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_order"):
        await update_order(UpdateOrderParams(id="ord-1", version=1), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_order_raises_context_error_for_customer_only(mock_api):
    # Customer-only context cannot create orders — only as-associate (customerId+businessUnitKey) can.
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="create_order"):
        await create_order(CreateOrderParams(cart_id="cart-1", version=1), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_order_raises_context_error_for_customer_only(mock_api):
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="update_order"):
        await update_order(UpdateOrderParams(id="ord-1", version=1), mock_api, ctx)


@pytest.mark.asyncio
async def test_read_order_succeeds_for_admin(mock_api):
    ctx = CTContext(is_admin=True)
    result = await read_order(ReadOrderParams(), mock_api, ctx)
    assert result is not None


@pytest.mark.asyncio
async def test_read_order_succeeds_for_customer(mock_api):
    ctx = CTContext(customer_id="cust-1")
    result = await read_order(ReadOrderParams(), mock_api, ctx)
    assert result is not None


@pytest.mark.asyncio
async def test_create_order_succeeds_for_associate(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    mock_api.post = AsyncMock(return_value={"id": "ord-1"})
    result = await create_order(CreateOrderParams(cart_id="cart-1", version=1), mock_api, ctx)
    assert result is not None
