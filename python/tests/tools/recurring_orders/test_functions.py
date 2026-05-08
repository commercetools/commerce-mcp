"""Tests for recurring_orders context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.recurring_orders.functions import (
    read_recurring_orders,
    create_recurring_orders,
    update_recurring_orders,
)
from commerce_mcp.tools.recurring_orders.schemas import (
    ReadRecurringOrdersParams,
    CreateRecurringOrdersParams,
    UpdateRecurringOrdersParams,
    RecurringOrderUpdateAction,
    _CartReference,
    _RecurrencePolicyReference,
    _Schedule,
)
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError, ContextError


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def customer_ctx():
    return CTContext(customer_id="cust-1")


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "ro-1", "version": 1})
    api.post = AsyncMock(return_value={"id": "ro-1", "version": 1})
    return api


@pytest.fixture
def mock_api_list():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "ro-1"}]})
    api.post = AsyncMock(return_value={"id": "ro-1", "version": 1})
    return api


@pytest.fixture
def cart_ref():
    return _CartReference(id="cart-1")


@pytest.fixture
def create_params(cart_ref):
    return CreateRecurringOrdersParams(cart=cart_ref, cart_version=1)


# ── Admin: read routing ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_recurring_orders_admin_by_id(mock_api, admin_ctx):
    await read_recurring_orders(ReadRecurringOrdersParams(id="ro-1"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/recurring-orders/ro-1"


@pytest.mark.asyncio
async def test_read_recurring_orders_admin_by_key(mock_api, admin_ctx):
    await read_recurring_orders(ReadRecurringOrdersParams(key="my-order"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/recurring-orders/key=my-order"


@pytest.mark.asyncio
async def test_read_recurring_orders_admin_list(mock_api_list, admin_ctx):
    await read_recurring_orders(ReadRecurringOrdersParams(), mock_api_list, admin_ctx)
    assert mock_api_list.get.call_args[0][0] == "/recurring-orders"


@pytest.mark.asyncio
async def test_read_recurring_orders_admin_list_with_where(mock_api_list, admin_ctx):
    await read_recurring_orders(
        ReadRecurringOrdersParams(where=['customerId="cust-1"']),
        mock_api_list,
        admin_ctx,
    )
    assert mock_api_list.get.call_args[0][0] == "/recurring-orders"
    params = mock_api_list.get.call_args[1]["params"]
    assert 'customerId="cust-1"' in str(params.get("where"))


# ── Customer: read routing ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_recurring_orders_customer_by_id_filters_by_customer(mock_api, customer_ctx):
    mock_api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "ro-1"}]})
    await read_recurring_orders(ReadRecurringOrdersParams(id="ro-1"), mock_api, customer_ctx)
    assert mock_api.get.call_args[0][0] == "/recurring-orders"
    params = mock_api.get.call_args[1]["params"]
    where_str = str(params.get("where"))
    assert 'id="ro-1"' in where_str
    assert 'customerId="cust-1"' in where_str


@pytest.mark.asyncio
async def test_read_recurring_orders_customer_by_key_filters_by_customer(mock_api, customer_ctx):
    mock_api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "ro-1"}]})
    await read_recurring_orders(ReadRecurringOrdersParams(key="my-order"), mock_api, customer_ctx)
    assert mock_api.get.call_args[0][0] == "/recurring-orders"
    params = mock_api.get.call_args[1]["params"]
    where_str = str(params.get("where"))
    assert 'key="my-order"' in where_str
    assert 'customerId="cust-1"' in where_str


@pytest.mark.asyncio
async def test_read_recurring_orders_customer_list_injects_customer_filter(customer_ctx):
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 0, "results": []})
    await read_recurring_orders(ReadRecurringOrdersParams(), api, customer_ctx)
    assert api.get.call_args[0][0] == "/recurring-orders"
    params = api.get.call_args[1]["params"]
    assert 'customerId="cust-1"' in str(params.get("where"))


@pytest.mark.asyncio
async def test_read_recurring_orders_customer_id_not_found_raises(mock_api, customer_ctx):
    mock_api.get = AsyncMock(return_value={"count": 0, "results": []})
    with pytest.raises(SDKError, match="read recurring orders"):
        await read_recurring_orders(ReadRecurringOrdersParams(id="ro-1"), mock_api, customer_ctx)


# ── ContextError: neither admin nor customer ──────────────────────────────────

@pytest.mark.asyncio
async def test_read_recurring_orders_no_context_raises_context_error(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_recurring_orders"):
        await read_recurring_orders(ReadRecurringOrdersParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


@pytest.mark.asyncio
async def test_read_recurring_orders_store_ctx_raises_context_error(mock_api):
    ctx = CTContext(store_key="my-store")
    with pytest.raises(ContextError, match="read_recurring_orders"):
        await read_recurring_orders(ReadRecurringOrdersParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


# ── Create: admin only ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_recurring_orders_admin_ok(mock_api, admin_ctx, create_params):
    await create_recurring_orders(create_params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/recurring-orders"


@pytest.mark.asyncio
async def test_create_recurring_orders_customer_raises_context_error(mock_api, customer_ctx, create_params):
    with pytest.raises(ContextError, match="create_recurring_orders"):
        await create_recurring_orders(create_params, mock_api, customer_ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_recurring_orders_no_context_raises_context_error(mock_api, create_params):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_recurring_orders"):
        await create_recurring_orders(create_params, mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Update: admin only ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_recurring_orders_admin_by_id(mock_api, admin_ctx):
    params = UpdateRecurringOrdersParams(
        id="ro-1",
        version=1,
        actions=[RecurringOrderUpdateAction(action="setState")],
    )
    await update_recurring_orders(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/recurring-orders/ro-1"


@pytest.mark.asyncio
async def test_update_recurring_orders_admin_by_key(mock_api, admin_ctx):
    params = UpdateRecurringOrdersParams(
        key="my-order",
        version=1,
        actions=[RecurringOrderUpdateAction(action="setState")],
    )
    await update_recurring_orders(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/recurring-orders/key=my-order"


@pytest.mark.asyncio
async def test_update_recurring_orders_customer_raises_context_error(mock_api, customer_ctx):
    params = UpdateRecurringOrdersParams(
        id="ro-1",
        version=1,
        actions=[RecurringOrderUpdateAction(action="setState")],
    )
    with pytest.raises(ContextError, match="update_recurring_orders"):
        await update_recurring_orders(params, mock_api, customer_ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_recurring_orders_no_context_raises_context_error(mock_api):
    ctx = CTContext()
    params = UpdateRecurringOrdersParams(
        id="ro-1",
        version=1,
        actions=[RecurringOrderUpdateAction(action="setState")],
    )
    with pytest.raises(ContextError, match="update_recurring_orders"):
        await update_recurring_orders(params, mock_api, ctx)
    mock_api.post.assert_not_called()


# ── SDK errors ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_recurring_orders_admin_sdk_error_on_failure(admin_ctx):
    api = MagicMock()
    api.get = AsyncMock(side_effect=Exception("500 Server Error"))
    with pytest.raises(SDKError, match="read recurring orders"):
        await read_recurring_orders(ReadRecurringOrdersParams(id="ro-1"), api, admin_ctx)


@pytest.mark.asyncio
async def test_read_recurring_orders_customer_sdk_error_on_failure(customer_ctx):
    api = MagicMock()
    api.get = AsyncMock(side_effect=Exception("500 Server Error"))
    with pytest.raises(SDKError, match="read recurring orders"):
        await read_recurring_orders(ReadRecurringOrdersParams(), api, customer_ctx)


@pytest.mark.asyncio
async def test_create_recurring_orders_sdk_error_on_failure(admin_ctx, create_params):
    api = MagicMock()
    api.post = AsyncMock(side_effect=Exception("500 Server Error"))
    with pytest.raises(SDKError, match="create recurring orders"):
        await create_recurring_orders(create_params, api, admin_ctx)


@pytest.mark.asyncio
async def test_update_recurring_orders_sdk_error_on_failure(admin_ctx):
    api = MagicMock()
    api.post = AsyncMock(side_effect=Exception("500 Server Error"))
    params = UpdateRecurringOrdersParams(
        id="ro-1",
        version=1,
        actions=[RecurringOrderUpdateAction(action="setState")],
    )
    with pytest.raises(SDKError, match="update recurring orders"):
        await update_recurring_orders(params, api, admin_ctx)
