"""Tests for carts context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.carts.functions import read_cart, create_cart, replicate_cart, update_cart
from commerce_mcp.tools.carts.schemas import (
    ReadCartParams, CreateCartParams, ReplicateCartParams,
    CartReference, UpdateCartParams,
)
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError, ContextError


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "cart-1"}]})
    api.post = AsyncMock(return_value={"id": "cart-1", "version": 2})
    return api


@pytest.fixture
def cart_owned_by_customer():
    return {"id": "cart-1", "customerId": "cust-1", "version": 1}


@pytest.fixture
def cart_owned_by_store():
    return {"id": "cart-1", "store": {"key": "eu-store", "typeId": "store"}, "version": 1}


# ── Admin: read routing ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_cart_admin_by_id(mock_api):
    ctx = CTContext(is_admin=True)
    await read_cart(ReadCartParams(id="cart-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/carts/cart-1"


@pytest.mark.asyncio
async def test_read_cart_admin_by_key(mock_api):
    ctx = CTContext(is_admin=True)
    await read_cart(ReadCartParams(key="my-cart"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/carts/key=my-cart"


@pytest.mark.asyncio
async def test_read_cart_admin_by_customer_id(mock_api):
    ctx = CTContext(is_admin=True)
    await read_cart(ReadCartParams(customer_id="cust-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/carts"
    params = mock_api.get.call_args[1]["params"]
    assert 'customerId="cust-1"' in str(params.get("where"))


@pytest.mark.asyncio
async def test_read_cart_admin_by_where(mock_api):
    ctx = CTContext(is_admin=True)
    await read_cart(ReadCartParams(where=['cartState="Active"']), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/carts"


@pytest.mark.asyncio
async def test_read_cart_admin_with_store_key_uses_in_store(mock_api):
    ctx = CTContext(is_admin=True)
    await read_cart(ReadCartParams(customer_id="cust-1", store_key="eu-store"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/carts"


@pytest.mark.asyncio
async def test_read_cart_admin_no_filter_raises(mock_api):
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to read cart"):
        await read_cart(ReadCartParams(), mock_api, ctx)


# ── Customer: read routing ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_cart_customer_default_filters_by_customer_id(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await read_cart(ReadCartParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/carts"
    params = mock_api.get.call_args[1]["params"]
    assert 'customerId="cust-1"' in str(params.get("where"))


@pytest.mark.asyncio
async def test_read_cart_customer_with_cart_id_in_context(mock_api):
    mock_api.get = AsyncMock(return_value={"id": "cart-1", "customerId": "cust-1"})
    ctx = CTContext(customer_id="cust-1", cart_id="cart-1")
    await read_cart(ReadCartParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/carts/cart-1"


@pytest.mark.asyncio
async def test_read_cart_customer_cart_not_owned_raises(mock_api):
    mock_api.get = AsyncMock(return_value={"id": "cart-1", "customerId": "other-cust"})
    ctx = CTContext(customer_id="cust-1", cart_id="cart-1")
    with pytest.raises(SDKError):
        await read_cart(ReadCartParams(), mock_api, ctx)


# ── Store: read routing ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_cart_store_default_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await read_cart(ReadCartParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/carts"


@pytest.mark.asyncio
async def test_read_cart_store_by_id_verifies_store(mock_api, cart_owned_by_store):
    mock_api.get = AsyncMock(return_value=cart_owned_by_store)
    ctx = CTContext(store_key="eu-store")
    await read_cart(ReadCartParams(id="cart-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/carts/cart-1"


@pytest.mark.asyncio
async def test_read_cart_store_id_wrong_store_raises(mock_api):
    mock_api.get = AsyncMock(return_value={"id": "cart-1", "store": {"key": "other-store"}})
    ctx = CTContext(store_key="eu-store")
    with pytest.raises(SDKError):
        await read_cart(ReadCartParams(id="cart-1"), mock_api, ctx)


# ── Associate: read routing ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_cart_routes_to_associate(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    await read_cart(ReadCartParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=bu-1" in path


@pytest.mark.asyncio
async def test_read_cart_associate_by_id(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    await read_cart(ReadCartParams(id="cart-1"), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert path.endswith("/carts/cart-1")


@pytest.mark.asyncio
async def test_read_cart_associate_by_key(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    await read_cart(ReadCartParams(key="my-cart"), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert path.endswith("/carts/key=my-cart")


# ── Create routing ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_cart_admin_uses_carts_path(mock_api):
    ctx = CTContext(is_admin=True)
    await create_cart(CreateCartParams(currency="USD"), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/carts"


@pytest.mark.asyncio
async def test_create_cart_admin_with_store_uses_in_store_path(mock_api):
    from commerce_mcp.tools.carts.schemas import CartStore
    ctx = CTContext(is_admin=True)
    params = CreateCartParams(currency="USD", store=CartStore(key="eu-store"))
    await create_cart(params, mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/carts"


@pytest.mark.asyncio
async def test_create_cart_customer_injects_customer_id(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await create_cart(CreateCartParams(currency="USD"), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/carts"
    body = mock_api.post.call_args[1]["body"]
    assert body.get("customerId") == "cust-1"


@pytest.mark.asyncio
async def test_create_cart_store_injects_store_and_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await create_cart(CreateCartParams(currency="EUR"), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/carts"
    body = mock_api.post.call_args[1]["body"]
    assert body.get("store", {}).get("key") == "eu-store"


@pytest.mark.asyncio
async def test_create_cart_associate_injects_customer_and_business_unit(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    await create_cart(CreateCartParams(currency="USD"), mock_api, ctx)
    path = mock_api.post.call_args[0][0]
    assert "as-associate/cust-1" in path
    body = mock_api.post.call_args[1]["body"]
    assert body.get("customerId") == "cust-1"
    assert body.get("businessUnit", {}).get("key") == "bu-1"


# ── Replicate routing ──────────────────────────────────────────────────────────

@pytest.fixture
def replicate_params():
    return ReplicateCartParams(reference=CartReference(id="cart-1"))


@pytest.mark.asyncio
async def test_replicate_cart_admin_uses_replicate_endpoint(mock_api, replicate_params):
    ctx = CTContext(is_admin=True)
    await replicate_cart(replicate_params, mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/carts/replicate"


@pytest.mark.asyncio
async def test_replicate_cart_admin_with_store_key(mock_api):
    ctx = CTContext(is_admin=True)
    params = ReplicateCartParams(reference=CartReference(id="cart-1"), store_key="eu-store")
    await replicate_cart(params, mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/carts/replicate"


@pytest.mark.asyncio
async def test_replicate_cart_customer_verifies_ownership(mock_api, cart_owned_by_customer, replicate_params):
    mock_api.get = AsyncMock(return_value=cart_owned_by_customer)
    ctx = CTContext(customer_id="cust-1")
    await replicate_cart(replicate_params, mock_api, ctx)
    mock_api.get.assert_called_once_with("/carts/cart-1")
    assert mock_api.post.call_args[0][0] == "/carts/replicate"


@pytest.mark.asyncio
async def test_replicate_cart_customer_wrong_owner_raises(mock_api, replicate_params):
    mock_api.get = AsyncMock(return_value={"id": "cart-1", "customerId": "other"})
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(SDKError):
        await replicate_cart(replicate_params, mock_api, ctx)


@pytest.mark.asyncio
async def test_replicate_cart_store_verifies_store(mock_api, cart_owned_by_store, replicate_params):
    mock_api.get = AsyncMock(return_value=cart_owned_by_store)
    ctx = CTContext(store_key="eu-store")
    await replicate_cart(replicate_params, mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/carts/replicate"


@pytest.mark.asyncio
async def test_replicate_cart_associate_uses_associate_path(mock_api, replicate_params):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    await replicate_cart(replicate_params, mock_api, ctx)
    path = mock_api.post.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert path.endswith("/carts/replicate")


# ── Update routing ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_cart_admin_by_id(mock_api):
    ctx = CTContext(is_admin=True)
    await update_cart(UpdateCartParams(id="cart-1", version=1), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/carts/cart-1"


@pytest.mark.asyncio
async def test_update_cart_admin_by_key(mock_api):
    ctx = CTContext(is_admin=True)
    await update_cart(UpdateCartParams(key="my-cart", version=1), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/carts/key=my-cart"


@pytest.mark.asyncio
async def test_update_cart_admin_with_store_key(mock_api):
    ctx = CTContext(is_admin=True)
    await update_cart(UpdateCartParams(id="cart-1", version=1, store_key="eu-store"), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/carts/cart-1"


@pytest.mark.asyncio
async def test_update_cart_customer_verifies_ownership(mock_api, cart_owned_by_customer):
    mock_api.get = AsyncMock(return_value=cart_owned_by_customer)
    ctx = CTContext(customer_id="cust-1")
    await update_cart(UpdateCartParams(id="cart-1", version=1), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/carts/cart-1"


@pytest.mark.asyncio
async def test_update_cart_customer_wrong_owner_raises(mock_api):
    mock_api.get = AsyncMock(return_value={"id": "cart-1", "customerId": "other"})
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(SDKError):
        await update_cart(UpdateCartParams(id="cart-1", version=1), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_cart_store_verifies_store(mock_api, cart_owned_by_store):
    mock_api.get = AsyncMock(return_value=cart_owned_by_store)
    ctx = CTContext(store_key="eu-store")
    await update_cart(UpdateCartParams(id="cart-1", version=1), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/carts/cart-1"


@pytest.mark.asyncio
async def test_update_cart_associate_by_id(mock_api):
    from commerce_mcp.tools.carts.schemas import CartUpdateAction
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    action = CartUpdateAction(action="setShippingAddress")
    await update_cart(UpdateCartParams(id="cart-1", version=1, actions=[action]), mock_api, ctx)
    path = mock_api.post.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert path.endswith("/carts/cart-1")


@pytest.mark.asyncio
async def test_update_cart_associate_by_key(mock_api):
    from commerce_mcp.tools.carts.schemas import CartUpdateAction
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    action = CartUpdateAction(action="setShippingAddress")
    await update_cart(UpdateCartParams(key="my-cart", version=1, actions=[action]), mock_api, ctx)
    path = mock_api.post.call_args[0][0]
    assert path.endswith("/carts/key=my-cart")


# ── Security: no fallthrough to admin ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_cart_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
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


@pytest.mark.asyncio
async def test_replicate_cart_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="replicate_cart"):
        await replicate_cart(ReplicateCartParams(reference=CartReference(id="cart-1")), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── SDK errors ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_cart_raises_sdk_error_on_failure(mock_api):
    mock_api.get.side_effect = Exception("500 Server Error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to read cart"):
        await read_cart(ReadCartParams(id="cart-1"), mock_api, ctx)
