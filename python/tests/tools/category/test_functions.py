"""Tests for category context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.category.functions import (
    read_category,
    create_category,
    update_category,
)
from commerce_mcp.tools.category.schemas import (
    ReadCategoryParams,
    CreateCategoryParams,
    UpdateCategoryParams,
    CategoryUpdateAction,
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
    api.get = AsyncMock(return_value={"id": "cat-1", "version": 1})
    api.post = AsyncMock(return_value={"id": "cat-1", "version": 1})
    return api


@pytest.fixture
def mock_api_list():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "cat-1"}]})
    api.post = AsyncMock(return_value={"id": "cat-1", "version": 1})
    return api


@pytest.fixture
def create_params():
    return CreateCategoryParams(
        name={"en": "Clothes"},
        slug={"en": "clothes"},
    )


# ── Read: no context guard (all contexts allowed) ─────────────────────────────

@pytest.mark.asyncio
async def test_read_category_admin_by_id(mock_api, admin_ctx):
    await read_category(ReadCategoryParams(id="cat-1"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/categories/cat-1"


@pytest.mark.asyncio
async def test_read_category_admin_by_key(mock_api, admin_ctx):
    await read_category(ReadCategoryParams(key="clothes"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/categories/key=clothes"


@pytest.mark.asyncio
async def test_read_category_admin_list(mock_api_list, admin_ctx):
    await read_category(ReadCategoryParams(), mock_api_list, admin_ctx)
    assert mock_api_list.get.call_args[0][0] == "/categories"


@pytest.mark.asyncio
async def test_read_category_customer_by_id(mock_api, customer_ctx):
    await read_category(ReadCategoryParams(id="cat-1"), mock_api, customer_ctx)
    assert mock_api.get.call_args[0][0] == "/categories/cat-1"


@pytest.mark.asyncio
async def test_read_category_customer_by_key(mock_api, customer_ctx):
    await read_category(ReadCategoryParams(key="clothes"), mock_api, customer_ctx)
    assert mock_api.get.call_args[0][0] == "/categories/key=clothes"


@pytest.mark.asyncio
async def test_read_category_customer_list(mock_api_list, customer_ctx):
    await read_category(ReadCategoryParams(), mock_api_list, customer_ctx)
    assert mock_api_list.get.call_args[0][0] == "/categories"


@pytest.mark.asyncio
async def test_read_category_empty_context_by_id(mock_api):
    ctx = CTContext()
    await read_category(ReadCategoryParams(id="cat-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/categories/cat-1"


@pytest.mark.asyncio
async def test_read_category_empty_context_by_key(mock_api):
    ctx = CTContext()
    await read_category(ReadCategoryParams(key="clothes"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/categories/key=clothes"


@pytest.mark.asyncio
async def test_read_category_empty_context_list(mock_api_list):
    ctx = CTContext()
    await read_category(ReadCategoryParams(), mock_api_list, ctx)
    assert mock_api_list.get.call_args[0][0] == "/categories"


@pytest.mark.asyncio
async def test_read_category_store_context_by_id(mock_api):
    ctx = CTContext(store_key="my-store")
    await read_category(ReadCategoryParams(id="cat-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/categories/cat-1"


@pytest.mark.asyncio
async def test_read_category_list_with_where(mock_api_list, admin_ctx):
    await read_category(
        ReadCategoryParams(where=['name(en = "Clothes")']),
        mock_api_list,
        admin_ctx,
    )
    assert mock_api_list.get.call_args[0][0] == "/categories"
    params = mock_api_list.get.call_args[1]["params"]
    assert 'name(en = "Clothes")' in str(params.get("where"))


# ── Create: admin only ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_category_admin_ok(mock_api, admin_ctx, create_params):
    await create_category(create_params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/categories"


@pytest.mark.asyncio
async def test_create_category_customer_raises_context_error(mock_api, customer_ctx, create_params):
    with pytest.raises(ContextError, match="create_category"):
        await create_category(create_params, mock_api, customer_ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_category_no_context_raises_context_error(mock_api, create_params):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_category"):
        await create_category(create_params, mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_category_store_context_raises_context_error(mock_api, create_params):
    ctx = CTContext(store_key="my-store")
    with pytest.raises(ContextError, match="create_category"):
        await create_category(create_params, mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Update: admin only ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_category_admin_by_id(mock_api, admin_ctx):
    params = UpdateCategoryParams(
        id="cat-1",
        version=1,
        actions=[CategoryUpdateAction(action="changeName")],
    )
    await update_category(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/categories/cat-1"


@pytest.mark.asyncio
async def test_update_category_admin_by_key(mock_api, admin_ctx):
    params = UpdateCategoryParams(
        key="clothes",
        version=1,
        actions=[CategoryUpdateAction(action="changeName")],
    )
    await update_category(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/categories/key=clothes"


@pytest.mark.asyncio
async def test_update_category_customer_raises_context_error(mock_api, customer_ctx):
    params = UpdateCategoryParams(
        id="cat-1",
        version=1,
        actions=[CategoryUpdateAction(action="changeName")],
    )
    with pytest.raises(ContextError, match="update_category"):
        await update_category(params, mock_api, customer_ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_category_no_context_raises_context_error(mock_api):
    ctx = CTContext()
    params = UpdateCategoryParams(
        id="cat-1",
        version=1,
        actions=[CategoryUpdateAction(action="changeName")],
    )
    with pytest.raises(ContextError, match="update_category"):
        await update_category(params, mock_api, ctx)
    mock_api.post.assert_not_called()


# ── SDK errors ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_category_sdk_error_on_failure():
    api = MagicMock()
    api.get = AsyncMock(side_effect=Exception("500 Server Error"))
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="read category"):
        await read_category(ReadCategoryParams(id="cat-1"), api, ctx)


@pytest.mark.asyncio
async def test_create_category_sdk_error_on_failure(admin_ctx, create_params):
    api = MagicMock()
    api.post = AsyncMock(side_effect=Exception("500 Server Error"))
    with pytest.raises(SDKError, match="create category"):
        await create_category(create_params, api, admin_ctx)


@pytest.mark.asyncio
async def test_update_category_sdk_error_on_failure(admin_ctx):
    api = MagicMock()
    api.post = AsyncMock(side_effect=Exception("500 Server Error"))
    params = UpdateCategoryParams(
        id="cat-1",
        version=1,
        actions=[CategoryUpdateAction(action="changeName")],
    )
    with pytest.raises(SDKError, match="update category"):
        await update_category(params, api, admin_ctx)
