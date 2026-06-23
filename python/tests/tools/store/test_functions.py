"""Tests for store context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.store.functions import (
    read_store,
    create_store,
    update_store,
)
from commerce_mcp.tools.store.schemas import (
    ReadStoreParams,
    CreateStoreParams,
    UpdateStoreParams,
    StoreUpdateAction,
)
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError, ContextError


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def store_ctx():
    return CTContext(store_key="my-store")


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "store-1", "key": "my-store", "version": 1})
    api.post = AsyncMock(return_value={"id": "store-1", "key": "my-store", "version": 2})
    return api


@pytest.fixture
def mock_api_list():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "store-1"}]})
    api.post = AsyncMock(return_value={"id": "store-1", "version": 2})
    return api


@pytest.fixture
def create_params():
    return CreateStoreParams(
        key="new-store",
        name={"en": "New Store"},
    )


# ── Admin: read routing ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_admin_by_id(mock_api, admin_ctx):
    await read_store(ReadStoreParams(id="store-1"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/stores/store-1"


@pytest.mark.asyncio
async def test_read_store_admin_by_key(mock_api, admin_ctx):
    await read_store(ReadStoreParams(key="my-store"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/stores/key=my-store"


@pytest.mark.asyncio
async def test_read_store_admin_list(mock_api_list, admin_ctx):
    await read_store(ReadStoreParams(), mock_api_list, admin_ctx)
    assert mock_api_list.get.call_args[0][0] == "/stores"


@pytest.mark.asyncio
async def test_read_store_admin_list_with_where(mock_api_list, admin_ctx):
    await read_store(
        ReadStoreParams(where=['name="My Store"']),
        mock_api_list,
        admin_ctx,
    )
    assert mock_api_list.get.call_args[0][0] == "/stores"
    params = mock_api_list.get.call_args[1]["params"]
    assert 'name="My Store"' in str(params.get("where"))


# ── Store-context: read own store ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_store_ctx_reads_own_store(mock_api, store_ctx):
    await read_store(ReadStoreParams(), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/stores/key=my-store"


@pytest.mark.asyncio
async def test_read_store_store_ctx_ignores_id_param(mock_api, store_ctx):
    # Store context always reads own store regardless of id/key in params
    await read_store(ReadStoreParams(id="other-store"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/stores/key=my-store"


# ── ContextError: no valid context ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_no_context_raises_context_error(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_store"):
        await read_store(ReadStoreParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


@pytest.mark.asyncio
async def test_read_store_customer_ctx_raises_context_error(mock_api):
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="read_store"):
        await read_store(ReadStoreParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


# ── Create: admin only ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_store_admin_ok(mock_api, admin_ctx, create_params):
    await create_store(create_params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/stores"


@pytest.mark.asyncio
async def test_create_store_store_ctx_raises_context_error(mock_api, store_ctx, create_params):
    with pytest.raises(ContextError, match="create_store"):
        await create_store(create_params, mock_api, store_ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_store_no_context_raises_context_error(mock_api, create_params):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_store"):
        await create_store(create_params, mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_store_customer_ctx_raises_context_error(mock_api, create_params):
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="create_store"):
        await create_store(create_params, mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Update: admin or store-context ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_store_admin_by_id(mock_api, admin_ctx):
    params = UpdateStoreParams(
        id="store-1",
        version=1,
        actions=[StoreUpdateAction(action="setName")],
    )
    await update_store(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/stores/store-1"


@pytest.mark.asyncio
async def test_update_store_admin_by_key(mock_api, admin_ctx):
    params = UpdateStoreParams(
        key="my-store",
        version=1,
        actions=[StoreUpdateAction(action="setName")],
    )
    await update_store(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/stores/key=my-store"


@pytest.mark.asyncio
async def test_update_store_store_ctx_updates_own_store(mock_api, store_ctx):
    params = UpdateStoreParams(
        version=1,
        actions=[StoreUpdateAction(action="setName")],
    )
    await update_store(params, mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/stores/key=my-store"


@pytest.mark.asyncio
async def test_update_store_no_context_raises_context_error(mock_api):
    ctx = CTContext()
    params = UpdateStoreParams(
        id="store-1",
        version=1,
        actions=[StoreUpdateAction(action="setName")],
    )
    with pytest.raises(ContextError, match="update_store"):
        await update_store(params, mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_store_customer_ctx_raises_context_error(mock_api):
    ctx = CTContext(customer_id="cust-1")
    params = UpdateStoreParams(
        id="store-1",
        version=1,
        actions=[StoreUpdateAction(action="setName")],
    )
    with pytest.raises(ContextError, match="update_store"):
        await update_store(params, mock_api, ctx)
    mock_api.post.assert_not_called()


# ── SDK errors ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_admin_sdk_error_on_failure(admin_ctx):
    api = MagicMock()
    api.get = AsyncMock(side_effect=Exception("500 Server Error"))
    with pytest.raises(SDKError, match="read store"):
        await read_store(ReadStoreParams(id="store-1"), api, admin_ctx)


@pytest.mark.asyncio
async def test_read_store_store_ctx_sdk_error_on_failure(store_ctx):
    api = MagicMock()
    api.get = AsyncMock(side_effect=Exception("500 Server Error"))
    with pytest.raises(SDKError, match="read store"):
        await read_store(ReadStoreParams(), api, store_ctx)


@pytest.mark.asyncio
async def test_create_store_sdk_error_on_failure(admin_ctx, create_params):
    api = MagicMock()
    api.post = AsyncMock(side_effect=Exception("500 Server Error"))
    with pytest.raises(SDKError, match="create store"):
        await create_store(create_params, api, admin_ctx)


@pytest.mark.asyncio
async def test_update_store_admin_sdk_error_on_failure(admin_ctx):
    api = MagicMock()
    api.post = AsyncMock(side_effect=Exception("500 Server Error"))
    params = UpdateStoreParams(
        id="store-1",
        version=1,
        actions=[StoreUpdateAction(action="setName")],
    )
    with pytest.raises(SDKError, match="update store"):
        await update_store(params, api, admin_ctx)


@pytest.mark.asyncio
async def test_update_store_store_ctx_sdk_error_on_failure(store_ctx):
    api = MagicMock()
    api.post = AsyncMock(side_effect=Exception("500 Server Error"))
    params = UpdateStoreParams(
        version=1,
        actions=[StoreUpdateAction(action="setName")],
    )
    with pytest.raises(SDKError, match="update store"):
        await update_store(params, api, store_ctx)
