"""Tests for cart_discount context-conditional dispatch."""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.cart_discount.functions import (
    read_cart_discount,
    create_cart_discount,
    update_cart_discount,
    _read_cart_discount_admin,
    _read_cart_discount_store,
    _create_cart_discount_admin,
    _create_cart_discount_store,
    _update_cart_discount_admin,
    _update_cart_discount_store,
)
from commerce_mcp.tools.cart_discount.schemas import (
    ReadCartDiscountParams,
    CreateCartDiscountParams,
    UpdateCartDiscountParams,
    CartDiscountUpdateAction,
)
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def store_ctx():
    return CTContext(store_key="my-store")


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "x-1"})
    api.post = AsyncMock(return_value={"id": "x-1", "version": 1})
    return api


def make_create_params() -> CreateCartDiscountParams:
    return CreateCartDiscountParams(
        name={"en": "Summer Sale"},
        cartPredicate="1=1",
        value={"type": "relative", "permyriad": 1000},
        sortOrder="0.5",
    )


def make_update_params(**kwargs) -> UpdateCartDiscountParams:
    return UpdateCartDiscountParams(
        id="cd-1",
        version=2,
        actions=[CartDiscountUpdateAction(action="changeIsActive")],
        **kwargs,
    )


# ── Dispatch: read_cart_discount ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await read_cart_discount(ReadCartDiscountParams(), mock_api, store_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=my-store/cart-discounts" in path


@pytest.mark.asyncio
async def test_read_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await read_cart_discount(ReadCartDiscountParams(), mock_api, admin_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert path == "/cart-discounts"


@pytest.mark.asyncio
async def test_read_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_cart_discount"):
        await read_cart_discount(ReadCartDiscountParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


# ── Dispatch: create_cart_discount ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await create_cart_discount(make_create_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/cart-discounts"


@pytest.mark.asyncio
async def test_create_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await create_cart_discount(make_create_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/cart-discounts"


@pytest.mark.asyncio
async def test_create_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_cart_discount"):
        await create_cart_discount(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Dispatch: update_cart_discount ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await update_cart_discount(make_update_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/in-store/key=my-store/cart-discounts/" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await update_cart_discount(make_update_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/cart-discounts/cd-1"


@pytest.mark.asyncio
async def test_update_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_cart_discount"):
        await update_cart_discount(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Admin read implementation ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_admin_list_uses_cart_discounts_endpoint(mock_api, admin_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_cart_discount_admin(ReadCartDiscountParams(), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/cart-discounts"


@pytest.mark.asyncio
async def test_read_admin_by_id_uses_direct_path(mock_api, admin_ctx):
    await _read_cart_discount_admin(ReadCartDiscountParams(id="cd-99"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/cart-discounts/cd-99"


@pytest.mark.asyncio
async def test_read_admin_by_key_uses_key_path(mock_api, admin_ctx):
    await _read_cart_discount_admin(ReadCartDiscountParams(key="my-key"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/cart-discounts/key=my-key"


@pytest.mark.asyncio
async def test_read_admin_passes_query_params(mock_api, admin_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_cart_discount_admin(
        ReadCartDiscountParams(limit=10, offset=5, sort=["sortOrder asc"]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 10
    assert params["offset"] == 5
    assert params["sort"] == ["sortOrder asc"]


@pytest.mark.asyncio
async def test_read_admin_with_where_filter(mock_api, admin_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_cart_discount_admin(
        ReadCartDiscountParams(where=["isActive=true"]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["where"] == ["isActive=true"]


@pytest.mark.asyncio
async def test_read_admin_with_expand(mock_api, admin_ctx):
    await _read_cart_discount_admin(
        ReadCartDiscountParams(id="cd-1", expand=["references[*]"]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["expand"] == ["references[*]"]


# ── Store read implementation ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_list_uses_in_store_path(mock_api, store_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_cart_discount_store(ReadCartDiscountParams(), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/cart-discounts"


@pytest.mark.asyncio
async def test_read_store_by_id_uses_in_store_path(mock_api, store_ctx):
    await _read_cart_discount_store(ReadCartDiscountParams(id="cd-2"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/cart-discounts/cd-2"


@pytest.mark.asyncio
async def test_read_store_by_key_uses_in_store_key_path(mock_api, store_ctx):
    await _read_cart_discount_store(ReadCartDiscountParams(key="cd-key"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/cart-discounts/key=cd-key"


@pytest.mark.asyncio
async def test_read_store_passes_query_params(mock_api, store_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_cart_discount_store(
        ReadCartDiscountParams(limit=15, offset=0, sort=["createdAt desc"]),
        mock_api,
        store_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 15
    assert params["sort"] == ["createdAt desc"]


# ── Admin create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_admin_posts_to_cart_discounts(mock_api, admin_ctx):
    await _create_cart_discount_admin(make_create_params(), mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/cart-discounts"
    body = mock_api.post.call_args[1]["body"]
    assert body["name"] == {"en": "Summer Sale"}
    assert body["cartPredicate"] == "1=1"
    assert body["sortOrder"] == "0.5"


# ── Store create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_store_posts_to_in_store_path(mock_api, store_ctx):
    await _create_cart_discount_store(make_create_params(), mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/cart-discounts"
    body = mock_api.post.call_args[1]["body"]
    assert body["name"] == {"en": "Summer Sale"}
    assert body["sortOrder"] == "0.5"


# ── Admin update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_admin_by_id_posts_to_direct_path(mock_api, admin_ctx):
    await _update_cart_discount_admin(make_update_params(), mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/cart-discounts/cd-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 2
    assert body["actions"][0]["action"] == "changeIsActive"


@pytest.mark.asyncio
async def test_update_admin_by_key_posts_to_key_path(mock_api, admin_ctx):
    params = UpdateCartDiscountParams(
        key="cd-key", version=3, actions=[CartDiscountUpdateAction(action="changeName")]
    )
    await _update_cart_discount_admin(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/cart-discounts/key=cd-key"


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_when_no_id_or_key(mock_api, admin_ctx):
    params = UpdateCartDiscountParams(
        version=1, actions=[CartDiscountUpdateAction(action="changeIsActive")]
    )
    with pytest.raises(SDKError, match="update cart discount"):
        await _update_cart_discount_admin(params, mock_api, admin_ctx)


# ── Store update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_store_by_id_posts_to_in_store_path(mock_api, store_ctx):
    await _update_cart_discount_store(make_update_params(), mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/cart-discounts/cd-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 2


@pytest.mark.asyncio
async def test_update_store_by_key_posts_to_in_store_key_path(mock_api, store_ctx):
    params = UpdateCartDiscountParams(
        key="cd-key", version=1, actions=[CartDiscountUpdateAction(action="changeIsActive")]
    )
    await _update_cart_discount_store(params, mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/cart-discounts/key=cd-key"


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_when_no_id_or_key(mock_api, store_ctx):
    params = UpdateCartDiscountParams(
        version=1, actions=[CartDiscountUpdateAction(action="changeIsActive")]
    )
    with pytest.raises(SDKError, match="update cart discount"):
        await _update_cart_discount_store(params, mock_api, store_ctx)


# ── SDK error wrapping ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read cart discount"):
        await _read_cart_discount_admin(ReadCartDiscountParams(id="cd-1"), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_read_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read cart discount"):
        await _read_cart_discount_store(ReadCartDiscountParams(id="cd-1"), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_create_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create cart discount"):
        await _create_cart_discount_admin(make_create_params(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_create_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create cart discount"):
        await _create_cart_discount_store(make_create_params(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update cart discount"):
        await _update_cart_discount_admin(make_update_params(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update cart discount"):
        await _update_cart_discount_store(make_update_params(), mock_api, store_ctx)


# ── store_key takes priority over is_admin ────────────────────────────────────

@pytest.mark.asyncio
async def test_read_uses_store_path_when_both_store_key_and_admin(mock_api):
    ctx = CTContext(is_admin=True, store_key="priority-store")
    await read_cart_discount(ReadCartDiscountParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=priority-store/cart-discounts" in path


@pytest.mark.asyncio
async def test_create_uses_store_path_when_both_store_key_and_admin(mock_api):
    ctx = CTContext(is_admin=True, store_key="priority-store")
    await create_cart_discount(make_create_params(), mock_api, ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=priority-store/cart-discounts"
