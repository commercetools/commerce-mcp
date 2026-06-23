"""Tests for shopping_lists context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.shopping_lists.functions import (
    read_shopping_list,
    create_shopping_list,
    update_shopping_list,
    _read_shopping_list_customer,
    _read_shopping_list_store,
    _read_shopping_list_admin,
    _create_shopping_list_customer,
    _create_shopping_list_store,
    _create_shopping_list_admin,
    _update_shopping_list_customer,
    _update_shopping_list_store,
    _update_shopping_list_admin,
)
from commerce_mcp.tools.shopping_lists.schemas import (
    ReadShoppingListParams,
    CreateShoppingListParams,
    UpdateShoppingListParams,
    ShoppingListUpdateAction,
)
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def customer_ctx():
    return CTContext(customer_id="cust-1")


@pytest.fixture
def store_ctx():
    return CTContext(store_key="my-store")


@pytest.fixture
def bu_ctx():
    return CTContext(customer_id="cust-1", business_unit_key="bu-key")


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "sl-1"}]})
    api.post = AsyncMock(return_value={"id": "sl-1", "version": 2})
    return api


def make_create_params(**kwargs) -> CreateShoppingListParams:
    return CreateShoppingListParams(name={"en": "My List"}, **kwargs)


def make_update_params(**kwargs) -> UpdateShoppingListParams:
    return UpdateShoppingListParams(
        id="sl-1",
        version=1,
        actions=[ShoppingListUpdateAction(action="changeName")],
        **kwargs,
    )


# ── Context dispatch: read_shopping_list ──────────────────────────────────────

@pytest.mark.asyncio
async def test_read_dispatches_to_customer_when_customer_id(mock_api, customer_ctx):
    await read_shopping_list(ReadShoppingListParams(), mock_api, customer_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/me/shopping-lists" in path


@pytest.mark.asyncio
async def test_read_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await read_shopping_list(ReadShoppingListParams(), mock_api, store_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=my-store/shopping-lists" in path


@pytest.mark.asyncio
async def test_read_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await read_shopping_list(ReadShoppingListParams(), mock_api, admin_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert path == "/shopping-lists"


@pytest.mark.asyncio
async def test_read_customer_takes_priority_over_store(mock_api):
    ctx = CTContext(customer_id="cust-1", store_key="my-store")
    await read_shopping_list(ReadShoppingListParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "/me/shopping-lists" in path


@pytest.mark.asyncio
async def test_read_bu_ctx_routes_to_customer(mock_api, bu_ctx):
    # business_unit_key alone doesn't change shopping list dispatch;
    # customer_id is still the trigger for the /me path.
    await read_shopping_list(ReadShoppingListParams(), mock_api, bu_ctx)
    path = mock_api.get.call_args[0][0]
    assert "/me/shopping-lists" in path


@pytest.mark.asyncio
async def test_read_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_shopping_list"):
        await read_shopping_list(ReadShoppingListParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


# ── Context dispatch: create_shopping_list ────────────────────────────────────

@pytest.mark.asyncio
async def test_create_dispatches_to_customer_when_customer_id(mock_api, customer_ctx):
    await create_shopping_list(make_create_params(), mock_api, customer_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/me/shopping-lists"


@pytest.mark.asyncio
async def test_create_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await create_shopping_list(make_create_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/shopping-lists"


@pytest.mark.asyncio
async def test_create_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await create_shopping_list(make_create_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/shopping-lists"


@pytest.mark.asyncio
async def test_create_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_shopping_list"):
        await create_shopping_list(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Context dispatch: update_shopping_list ────────────────────────────────────

@pytest.mark.asyncio
async def test_update_dispatches_to_customer_when_customer_id(mock_api, customer_ctx):
    await update_shopping_list(make_update_params(), mock_api, customer_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/me/shopping-lists/" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await update_shopping_list(make_update_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/in-store/key=my-store/shopping-lists/" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await update_shopping_list(make_update_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/shopping-lists/sl-1" in path


@pytest.mark.asyncio
async def test_update_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_shopping_list"):
        await update_shopping_list(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Customer read implementation ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_customer_list_uses_me_endpoint(mock_api, customer_ctx):
    await _read_shopping_list_customer(ReadShoppingListParams(), mock_api, customer_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/me/shopping-lists"


@pytest.mark.asyncio
async def test_read_customer_injects_customer_where_filter(mock_api, customer_ctx):
    await _read_shopping_list_customer(ReadShoppingListParams(), mock_api, customer_ctx)
    params = mock_api.get.call_args[1]["params"]
    where = params.get("where", [])
    assert any("cust-1" in c for c in where)


@pytest.mark.asyncio
async def test_read_customer_by_id_uses_me_id_path(mock_api, customer_ctx):
    mock_api.get.return_value = {"id": "sl-1"}
    await _read_shopping_list_customer(ReadShoppingListParams(id="sl-1"), mock_api, customer_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/me/shopping-lists/sl-1"


@pytest.mark.asyncio
async def test_read_customer_by_key_uses_me_key_path(mock_api, customer_ctx):
    mock_api.get.return_value = {"id": "sl-1"}
    await _read_shopping_list_customer(ReadShoppingListParams(key="my-key"), mock_api, customer_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/me/shopping-lists/key=my-key"


@pytest.mark.asyncio
async def test_read_customer_passes_limit_offset_sort(mock_api, customer_ctx):
    await _read_shopping_list_customer(
        ReadShoppingListParams(limit=10, offset=5, sort=["name asc"]),
        mock_api,
        customer_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 10
    assert params["offset"] == 5
    assert params["sort"] == ["name asc"]


@pytest.mark.asyncio
async def test_read_customer_merges_extra_where(mock_api, customer_ctx):
    await _read_shopping_list_customer(
        ReadShoppingListParams(where=['name(en="Test")']),
        mock_api,
        customer_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    where = params["where"]
    assert any("cust-1" in c for c in where)
    assert any('name(en="Test")' in c for c in where)


# ── Store read implementation ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_list_uses_in_store_path(mock_api, store_ctx):
    await _read_shopping_list_store(ReadShoppingListParams(), mock_api, store_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/in-store/key=my-store/shopping-lists"


@pytest.mark.asyncio
async def test_read_store_by_id_uses_in_store_id_path(mock_api, store_ctx):
    mock_api.get.return_value = {"id": "sl-1"}
    await _read_shopping_list_store(ReadShoppingListParams(id="sl-1"), mock_api, store_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/in-store/key=my-store/shopping-lists/sl-1"


@pytest.mark.asyncio
async def test_read_store_by_key_uses_in_store_key_path(mock_api, store_ctx):
    mock_api.get.return_value = {"id": "sl-1"}
    await _read_shopping_list_store(ReadShoppingListParams(key="sl-key"), mock_api, store_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/in-store/key=my-store/shopping-lists/key=sl-key"


@pytest.mark.asyncio
async def test_read_store_passes_where_filter(mock_api, store_ctx):
    await _read_shopping_list_store(
        ReadShoppingListParams(where=['name(en="Test")']),
        mock_api,
        store_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["where"] == ['name(en="Test")']


# ── Admin read implementation ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_admin_list_uses_shopping_lists_endpoint(mock_api, admin_ctx):
    await _read_shopping_list_admin(ReadShoppingListParams(), mock_api, admin_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/shopping-lists"


@pytest.mark.asyncio
async def test_read_admin_by_id_uses_direct_path(mock_api, admin_ctx):
    mock_api.get.return_value = {"id": "sl-99"}
    await _read_shopping_list_admin(ReadShoppingListParams(id="sl-99"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/shopping-lists/sl-99"


@pytest.mark.asyncio
async def test_read_admin_by_key_uses_key_path(mock_api, admin_ctx):
    mock_api.get.return_value = {"id": "sl-99"}
    await _read_shopping_list_admin(ReadShoppingListParams(key="my-key"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/shopping-lists/key=my-key"


@pytest.mark.asyncio
async def test_read_admin_with_store_key_param_routes_to_in_store(mock_api, admin_ctx):
    await _read_shopping_list_admin(
        ReadShoppingListParams(store_key="eu-store"),
        mock_api,
        admin_ctx,
    )
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=eu-store/shopping-lists" in path


@pytest.mark.asyncio
async def test_read_admin_passes_limit_offset(mock_api, admin_ctx):
    await _read_shopping_list_admin(
        ReadShoppingListParams(limit=25, offset=50, sort=["createdAt desc"]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 25
    assert params["offset"] == 50
    assert params["sort"] == ["createdAt desc"]


# ── Customer create implementation ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_customer_posts_to_me_endpoint(mock_api, customer_ctx):
    await _create_shopping_list_customer(make_create_params(), mock_api, customer_ctx)
    assert mock_api.post.call_args[0][0] == "/me/shopping-lists"


@pytest.mark.asyncio
async def test_create_customer_injects_customer_ref_when_missing(mock_api, customer_ctx):
    await _create_shopping_list_customer(make_create_params(), mock_api, customer_ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["customer"]["id"] == "cust-1"
    assert body["customer"]["typeId"] == "customer"


@pytest.mark.asyncio
async def test_create_customer_does_not_override_existing_customer(mock_api, customer_ctx):
    from commerce_mcp.tools.shopping_lists.schemas import CustomerReference
    params = make_create_params(customer=CustomerReference(id="other-cust"))
    await _create_shopping_list_customer(params, mock_api, customer_ctx)
    body = mock_api.post.call_args[1]["body"]
    # existing customer reference is preserved
    assert body["customer"]["id"] == "other-cust"


# ── Store create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_store_posts_to_in_store_path(mock_api, store_ctx):
    await _create_shopping_list_store(make_create_params(), mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/shopping-lists"


@pytest.mark.asyncio
async def test_create_store_injects_store_ref_when_missing(mock_api, store_ctx):
    await _create_shopping_list_store(make_create_params(), mock_api, store_ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["store"]["key"] == "my-store"
    assert body["store"]["typeId"] == "store"


# ── Admin create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_admin_posts_to_shopping_lists(mock_api, admin_ctx):
    await _create_shopping_list_admin(make_create_params(), mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/shopping-lists"


@pytest.mark.asyncio
async def test_create_admin_with_store_key_param_uses_in_store_path(mock_api, admin_ctx):
    await _create_shopping_list_admin(
        make_create_params(store_key="eu-store"),
        mock_api,
        admin_ctx,
    )
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/shopping-lists"


# ── Customer update implementation ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_customer_by_id_posts_to_me_id_path(mock_api, customer_ctx):
    await _update_shopping_list_customer(make_update_params(), mock_api, customer_ctx)
    assert mock_api.post.call_args[0][0] == "/me/shopping-lists/sl-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1
    assert body["actions"][0]["action"] == "changeName"


@pytest.mark.asyncio
async def test_update_customer_by_key_posts_to_me_key_path(mock_api, customer_ctx):
    params = UpdateShoppingListParams(
        key="sl-key",
        version=3,
        actions=[ShoppingListUpdateAction(action="changeName")],
    )
    await _update_shopping_list_customer(params, mock_api, customer_ctx)
    assert mock_api.post.call_args[0][0] == "/me/shopping-lists/key=sl-key"


@pytest.mark.asyncio
async def test_update_customer_raises_sdk_error_when_no_id_or_key(mock_api, customer_ctx):
    params = UpdateShoppingListParams(
        version=1,
        actions=[ShoppingListUpdateAction(action="changeName")],
    )
    with pytest.raises(SDKError, match="update shopping list"):
        await _update_shopping_list_customer(params, mock_api, customer_ctx)


# ── Store update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_store_by_id_posts_to_in_store_path(mock_api, store_ctx):
    await _update_shopping_list_store(make_update_params(), mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/shopping-lists/sl-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1


@pytest.mark.asyncio
async def test_update_store_by_key_posts_to_in_store_key_path(mock_api, store_ctx):
    params = UpdateShoppingListParams(
        key="sl-key",
        version=2,
        actions=[ShoppingListUpdateAction(action="changeName")],
    )
    await _update_shopping_list_store(params, mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/shopping-lists/key=sl-key"


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_when_no_id_or_key(mock_api, store_ctx):
    params = UpdateShoppingListParams(
        version=1,
        actions=[ShoppingListUpdateAction(action="changeName")],
    )
    with pytest.raises(SDKError, match="update shopping list"):
        await _update_shopping_list_store(params, mock_api, store_ctx)


# ── Admin update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_admin_by_id_posts_to_direct_path(mock_api, admin_ctx):
    await _update_shopping_list_admin(make_update_params(), mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/shopping-lists/sl-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1
    assert body["actions"][0]["action"] == "changeName"


@pytest.mark.asyncio
async def test_update_admin_by_key_posts_to_key_path(mock_api, admin_ctx):
    params = UpdateShoppingListParams(
        key="sl-key",
        version=3,
        actions=[ShoppingListUpdateAction(action="changeName")],
    )
    await _update_shopping_list_admin(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/shopping-lists/key=sl-key"


@pytest.mark.asyncio
async def test_update_admin_with_store_key_param_uses_prefix(mock_api, admin_ctx):
    await _update_shopping_list_admin(
        make_update_params(store_key="eu-store"),
        mock_api,
        admin_ctx,
    )
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/shopping-lists/sl-1"


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_when_no_id_or_key(mock_api, admin_ctx):
    params = UpdateShoppingListParams(
        version=1,
        actions=[ShoppingListUpdateAction(action="changeName")],
    )
    with pytest.raises(SDKError, match="update shopping list"):
        await _update_shopping_list_admin(params, mock_api, admin_ctx)


# ── SDK error wrapping ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_customer_raises_sdk_error_on_api_failure(mock_api, customer_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read shopping list"):
        await _read_shopping_list_customer(ReadShoppingListParams(), mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_read_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read shopping list"):
        await _read_shopping_list_store(ReadShoppingListParams(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_read_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read shopping list"):
        await _read_shopping_list_admin(ReadShoppingListParams(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_create_customer_raises_sdk_error_on_api_failure(mock_api, customer_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create shopping list"):
        await _create_shopping_list_customer(make_create_params(), mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_create_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create shopping list"):
        await _create_shopping_list_store(make_create_params(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_create_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create shopping list"):
        await _create_shopping_list_admin(make_create_params(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_update_customer_raises_sdk_error_on_api_failure(mock_api, customer_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update shopping list"):
        await _update_shopping_list_customer(make_update_params(), mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update shopping list"):
        await _update_shopping_list_store(make_update_params(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update shopping list"):
        await _update_shopping_list_admin(make_update_params(), mock_api, admin_ctx)


# ── Security: no admin fallthrough ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_does_not_fallthrough_to_admin(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError):
        await read_shopping_list(ReadShoppingListParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


@pytest.mark.asyncio
async def test_create_does_not_fallthrough_to_admin(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError):
        await create_shopping_list(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_does_not_fallthrough_to_admin(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError):
        await update_shopping_list(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()
