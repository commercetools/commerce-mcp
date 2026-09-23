"""Tests for orders context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from commerce_mcp.tools.orders.functions import read_order, create_order, update_order
from commerce_mcp.tools.orders import admin_functions, customer_functions, store_functions, as_associate_functions
from commerce_mcp.tools.orders.schemas import ReadOrderParams, CreateOrderParams, UpdateOrderParams, OrderUpdateAction
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError, ContextError


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "order-123"}]})
    api.post = AsyncMock(return_value={"id": "order-123", "version": 2})
    return api


def make_update_params(**kwargs) -> UpdateOrderParams:
    return UpdateOrderParams(
        id="ord-1",
        version=1,
        actions=[OrderUpdateAction(action="addPayment")],
        **kwargs,
    )


# ── Context-conditional dispatch ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_order_dispatches_to_admin(mock_api):
    ctx = CTContext(is_admin=True)
    with patch(
        "commerce_mcp.tools.orders.functions.admin_functions.read_order",
        new=AsyncMock(return_value="admin result"),
    ) as mock_fn:
        await read_order(ReadOrderParams(), mock_api, ctx)
        mock_fn.assert_called_once()


@pytest.mark.asyncio
async def test_read_order_dispatches_to_customer(mock_api):
    ctx = CTContext(customer_id="cust-1")
    with patch(
        "commerce_mcp.tools.orders.functions.customer_functions.read_order",
        new=AsyncMock(return_value="customer result"),
    ) as mock_fn:
        await read_order(ReadOrderParams(), mock_api, ctx)
        mock_fn.assert_called_once()


@pytest.mark.asyncio
async def test_read_order_dispatches_to_store(mock_api):
    ctx = CTContext(store_key="my-store")
    with patch(
        "commerce_mcp.tools.orders.functions.store_functions.read_order",
        new=AsyncMock(return_value="store result"),
    ) as mock_fn:
        await read_order(ReadOrderParams(), mock_api, ctx)
        mock_fn.assert_called_once()


@pytest.mark.asyncio
async def test_read_order_dispatches_to_associate_when_both_set(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-key")
    with patch(
        "commerce_mcp.tools.orders.functions.as_associate_functions.read_order",
        new=AsyncMock(return_value="associate result"),
    ) as mock_fn:
        await read_order(ReadOrderParams(), mock_api, ctx)
        mock_fn.assert_called_once()


@pytest.mark.asyncio
async def test_create_order_dispatches_associate_over_store(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-key", store_key="s")
    with patch(
        "commerce_mcp.tools.orders.functions.as_associate_functions.create_order",
        new=AsyncMock(return_value="associate result"),
    ) as mock_fn:
        await create_order(CreateOrderParams(version=1), mock_api, ctx)
        mock_fn.assert_called_once()


# ── admin_functions implementation ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_order_admin_list_uses_orders_endpoint(mock_api):
    ctx = CTContext(is_admin=True)
    await admin_functions.read_order(ReadOrderParams(limit=5), mock_api, ctx)
    call_path = mock_api.get.call_args[0][0]
    assert call_path == "/orders"
    assert mock_api.get.call_args[1]["params"]["limit"] == 5


@pytest.mark.asyncio
async def test_read_order_admin_by_id_uses_direct_path(mock_api):
    mock_api.get.return_value = {"id": "order-123"}
    ctx = CTContext(is_admin=True)
    await admin_functions.read_order(ReadOrderParams(id="order-123"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/orders/order-123"


@pytest.mark.asyncio
async def test_read_order_admin_by_order_number_uses_direct_path(mock_api):
    mock_api.get.return_value = {"id": "order-123"}
    ctx = CTContext(is_admin=True)
    await admin_functions.read_order(
        ReadOrderParams(order_number="1001"), mock_api, ctx
    )
    assert mock_api.get.call_args[0][0] == "/orders/order-number=1001"


@pytest.mark.asyncio
async def test_read_order_admin_with_store_key_param_uses_in_store_path(mock_api):
    ctx = CTContext(is_admin=True)
    await admin_functions.read_order(
        ReadOrderParams(store_key="eu-store"), mock_api, ctx
    )
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/orders"


@pytest.mark.asyncio
async def test_read_order_admin_passes_sort_expand_offset(mock_api):
    ctx = CTContext(is_admin=True)
    await admin_functions.read_order(
        ReadOrderParams(sort=["createdAt desc"], expand=["customer"], offset=20),
        mock_api,
        ctx,
    )
    p = mock_api.get.call_args[1]["params"]
    assert p["sort"] == ["createdAt desc"]
    assert p["expand"] == ["customer"]
    assert p["offset"] == 20


# ── customer_functions implementation ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_order_customer_filters_by_customer_id(mock_api):
    ctx = CTContext(customer_id="cust-42")
    await customer_functions.read_order(ReadOrderParams(), mock_api, ctx)
    where = mock_api.get.call_args[1]["params"].get("where", [])
    assert any("cust-42" in clause for clause in where)


@pytest.mark.asyncio
async def test_read_order_customer_by_id_adds_customer_filter(mock_api):
    mock_api.get.return_value = {"count": 1, "results": [{"id": "o1"}]}
    ctx = CTContext(customer_id="cust-1")
    await customer_functions.read_order(ReadOrderParams(id="o1"), mock_api, ctx)
    where = mock_api.get.call_args[1]["params"].get("where", [])
    assert any('id="o1"' in c for c in where)
    assert any("cust-1" in c for c in where)


@pytest.mark.asyncio
async def test_read_order_customer_by_order_number_adds_customer_filter(mock_api):
    mock_api.get.return_value = {"count": 1, "results": [{"id": "o1"}]}
    ctx = CTContext(customer_id="cust-1")
    await customer_functions.read_order(
        ReadOrderParams(order_number="1001"), mock_api, ctx
    )
    where = mock_api.get.call_args[1]["params"].get("where", [])
    assert any("1001" in c for c in where)
    assert any("cust-1" in c for c in where)


# ── store_functions implementation ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_order_store_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await store_functions.read_order(ReadOrderParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/orders"


@pytest.mark.asyncio
async def test_read_order_store_by_id_uses_direct_path(mock_api):
    mock_api.get.return_value = {"id": "o1"}
    ctx = CTContext(store_key="eu-store")
    await store_functions.read_order(ReadOrderParams(id="o1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/orders/o1"


@pytest.mark.asyncio
async def test_create_order_store_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await store_functions.create_order(CreateOrderParams(id="cart-1", version=1), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/orders"


@pytest.mark.asyncio
async def test_update_order_store_by_id_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await store_functions.update_order(make_update_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/orders/ord-1"


@pytest.mark.asyncio
async def test_update_order_store_by_order_number(mock_api):
    ctx = CTContext(store_key="eu-store")
    params = UpdateOrderParams(order_number="1001", version=1, actions=[])
    await store_functions.update_order(params, mock_api, ctx)
    assert "order-number=1001" in mock_api.post.call_args[0][0]


# ── as_associate_functions implementation ─────────────────────────────────────

@pytest.mark.asyncio
async def test_read_order_associate_uses_as_associate_path(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="my-bu")
    await as_associate_functions.read_order(ReadOrderParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=my-bu" in path


@pytest.mark.asyncio
async def test_read_order_associate_by_id_uses_direct_path(mock_api):
    mock_api.get.return_value = {"id": "o1"}
    ctx = CTContext(customer_id="cust-1", business_unit_key="my-bu")
    await as_associate_functions.read_order(ReadOrderParams(id="o1"), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert path.endswith("/orders/o1")


@pytest.mark.asyncio
async def test_create_order_associate_cart_uses_associate_path(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="my-bu")
    await as_associate_functions.create_order(
        CreateOrderParams(id="cart-1", version=1), mock_api, ctx
    )
    path = mock_api.post.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=my-bu" in path
    assert path.endswith("/orders")


@pytest.mark.asyncio
async def test_create_order_associate_quote_uses_order_quote_path(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="my-bu")
    await as_associate_functions.create_order(
        CreateOrderParams(quote_id="q-1", version=1), mock_api, ctx
    )
    path = mock_api.post.call_args[0][0]
    assert path.endswith("/orders/order-quote")


@pytest.mark.asyncio
async def test_update_order_associate_by_id(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="my-bu")
    await as_associate_functions.update_order(make_update_params(), mock_api, ctx)
    path = mock_api.post.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert path.endswith("/orders/ord-1")


# ── admin create_order ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_order_admin_cart_posts_to_orders(mock_api):
    ctx = CTContext(is_admin=True)
    await admin_functions.create_order(
        CreateOrderParams(id="cart-1", version=1), mock_api, ctx
    )
    assert mock_api.post.call_args[0][0] == "/orders"
    body = mock_api.post.call_args[1]["body"]
    assert body["cart"]["id"] == "cart-1"
    assert body["version"] == 1


@pytest.mark.asyncio
async def test_create_order_admin_import_posts_to_orders_import(mock_api):
    from commerce_mcp.tools.orders.schemas import TotalPrice
    ctx = CTContext(is_admin=True)
    await admin_functions.create_order(
        CreateOrderParams(
            version=1,
            total_price=TotalPrice(currencyCode="EUR", centAmount=1000),
            customer_id="cust-1",
        ),
        mock_api,
        ctx,
    )
    assert mock_api.post.call_args[0][0] == "/orders/import"


@pytest.mark.asyncio
async def test_create_order_admin_quote_sends_quote_ref(mock_api):
    ctx = CTContext(is_admin=True)
    await admin_functions.create_order(
        CreateOrderParams(quote_id="q-1", version=2), mock_api, ctx
    )
    body = mock_api.post.call_args[1]["body"]
    assert body["quote"]["id"] == "q-1"
    assert body["quote"]["typeId"] == "quote"


# ── admin update_order ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_order_admin_by_id(mock_api):
    ctx = CTContext(is_admin=True)
    await admin_functions.update_order(make_update_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/orders/ord-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1
    assert body["actions"][0]["action"] == "addPayment"


@pytest.mark.asyncio
async def test_update_order_admin_by_order_number(mock_api):
    ctx = CTContext(is_admin=True)
    params = UpdateOrderParams(order_number="1001", version=1, actions=[])
    await admin_functions.update_order(params, mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/orders/order-number=1001"


@pytest.mark.asyncio
async def test_update_order_admin_with_store_key_uses_prefix(mock_api):
    ctx = CTContext(is_admin=True)
    await admin_functions.update_order(
        make_update_params(store_key="eu-store"), mock_api, ctx
    )
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/orders/ord-1"


# ── SDK error wrapping ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_order_raises_sdk_error(mock_api):
    mock_api.get.side_effect = Exception("Network error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to read order"):
        await admin_functions.read_order(ReadOrderParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_order_raises_sdk_error(mock_api):
    mock_api.post.side_effect = Exception("500")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to create order"):
        await admin_functions.create_order(CreateOrderParams(version=1), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_order_raises_sdk_error(mock_api):
    mock_api.post.side_effect = Exception("500")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to update order"):
        await admin_functions.update_order(make_update_params(), mock_api, ctx)


# ── Security: no fallthrough to admin when context is missing ─────────────────

@pytest.mark.asyncio
async def test_read_order_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_order"):
        await read_order(ReadOrderParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_order_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_order"):
        await create_order(CreateOrderParams(version=1), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_order_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_order"):
        await update_order(make_update_params(), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_order_raises_context_error_for_customer_only(mock_api):
    # Customer-only context cannot create orders — only as-associate can.
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="create_order"):
        await create_order(CreateOrderParams(version=1), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_order_raises_context_error_for_customer_only(mock_api):
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="update_order"):
        await update_order(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── All contexts succeed ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_order_succeeds_for_admin(mock_api):
    result = await read_order(ReadOrderParams(), mock_api, CTContext(is_admin=True))
    assert result is not None


@pytest.mark.asyncio
async def test_read_order_succeeds_for_customer(mock_api):
    result = await read_order(ReadOrderParams(), mock_api, CTContext(customer_id="cust-1"))
    assert result is not None


@pytest.mark.asyncio
async def test_read_order_succeeds_for_store(mock_api):
    result = await read_order(ReadOrderParams(), mock_api, CTContext(store_key="s"))
    assert result is not None


@pytest.mark.asyncio
async def test_create_order_succeeds_for_associate(mock_api):
    mock_api.post = AsyncMock(return_value={"id": "ord-1"})
    result = await create_order(
        CreateOrderParams(id="cart-1", version=1),
        mock_api,
        CTContext(customer_id="cust-1", business_unit_key="bu-1"),
    )
    assert result is not None
