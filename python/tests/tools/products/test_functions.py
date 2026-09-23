"""Unit tests for products functions — mirrors typescript/src/shared/products/test/."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.products.functions import list_products, create_product, update_product
from commerce_mcp.tools.products.schemas import (
    ListProductsParams,
    CreateProductParams,
    UpdateProductParams,
    ProductTypeReference,
    ProductUpdateAction,
)
from commerce_mcp.shared.errors import SDKError, ContextError


def make_product_params(**kwargs) -> CreateProductParams:
    return CreateProductParams(
        product_type=ProductTypeReference(id="pt-1"),
        name={"en": "Widget"},
        slug={"en": "widget"},
        **kwargs,
    )


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "prod-1", "version": 1}]})
    api.post = AsyncMock(return_value={"id": "prod-1", "version": 2})
    return api


# ── list_products ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_products_calls_get(mock_api, admin_context):
    params = ListProductsParams(limit=10)
    result = await list_products(params, mock_api, admin_context)
    mock_api.get.assert_called_once()
    call_args = mock_api.get.call_args
    assert call_args[0][0] == "/products"
    assert "prod-1" in result


@pytest.mark.asyncio
async def test_list_products_with_id_uses_direct_path(mock_api, admin_context):
    mock_api.get.return_value = {"id": "prod-1", "version": 1}
    params = ListProductsParams(id="prod-1")
    await list_products(params, mock_api, admin_context)
    call_path = mock_api.get.call_args[0][0]
    assert call_path == "/products/prod-1"


@pytest.mark.asyncio
async def test_list_products_with_id_passes_expand(mock_api, admin_context):
    mock_api.get.return_value = {"id": "prod-1", "version": 1}
    params = ListProductsParams(id="prod-1", expand=["masterData.current.categories[*]"])
    await list_products(params, mock_api, admin_context)
    query = mock_api.get.call_args[1]["params"]
    assert query["expand"] == ["masterData.current.categories[*]"]


@pytest.mark.asyncio
async def test_list_products_default_limit_is_10(mock_api, admin_context):
    await list_products(ListProductsParams(), mock_api, admin_context)
    query = mock_api.get.call_args[1]["params"]
    assert query["limit"] == 10


@pytest.mark.asyncio
async def test_list_products_raises_sdk_error_on_failure(mock_api, admin_context):
    mock_api.get.side_effect = Exception("500 Internal Server Error")
    with pytest.raises(SDKError, match="Failed to list products"):
        await list_products(ListProductsParams(), mock_api, admin_context)


@pytest.mark.asyncio
async def test_list_products_returns_json(mock_api, admin_context):
    mock_api.get.return_value = {"count": 1, "results": [{"id": "p1", "key": "widget"}]}
    result = await list_products(ListProductsParams(), mock_api, admin_context)
    assert '"id"' in result


# ── create_product ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_product_calls_post(mock_api, admin_context):
    params = make_product_params()
    result = await create_product(params, mock_api, admin_context)
    mock_api.post.assert_called_once()
    assert "prod-1" in result


@pytest.mark.asyncio
async def test_create_product_serializes_product_type_reference(mock_api, admin_context):
    params = make_product_params()
    await create_product(params, mock_api, admin_context)
    body = mock_api.post.call_args[1]["body"]
    assert body["productType"] == {"id": "pt-1", "typeId": "product-type"}


@pytest.mark.asyncio
async def test_create_product_raises_sdk_error(mock_api, admin_context):
    mock_api.post.side_effect = Exception("400 Bad Request")
    with pytest.raises(SDKError, match="Failed to create product"):
        await create_product(make_product_params(), mock_api, admin_context)


# ── update_product ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_product_calls_post_with_correct_path(mock_api, admin_context):
    params = UpdateProductParams(
        id="prod-1",
        version=1,
        actions=[ProductUpdateAction(action="publish")],
    )
    await update_product(params, mock_api, admin_context)
    call_path = mock_api.post.call_args[0][0]
    assert call_path == "/products/prod-1"


@pytest.mark.asyncio
async def test_update_product_sends_version_and_actions(mock_api, admin_context):
    params = UpdateProductParams(
        id="prod-1",
        version=3,
        actions=[ProductUpdateAction(action="setKey", key="new-key")],
    )
    await update_product(params, mock_api, admin_context)
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 3
    assert body["actions"][0]["action"] == "setKey"


# ── Security: create/update require isAdmin — mirrors contextToProductFunctionMapping ──

@pytest.mark.asyncio
async def test_create_product_raises_context_error_without_admin(mock_api):
    from commerce_mcp.config import CTContext
    ctx = CTContext()  # is_admin=False by default
    with pytest.raises(ContextError, match="create_product"):
        await create_product(make_product_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_product_raises_context_error_for_customer_context(mock_api):
    from commerce_mcp.config import CTContext
    ctx = CTContext(customer_id="cust-1")  # customer context, not admin
    with pytest.raises(ContextError, match="create_product"):
        await create_product(make_product_params(), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_product_raises_context_error_without_admin(mock_api):
    from commerce_mcp.config import CTContext
    ctx = CTContext()
    params = UpdateProductParams(
        id="prod-1",
        version=1,
        actions=[ProductUpdateAction(action="publish")],
    )
    with pytest.raises(ContextError, match="update_product"):
        await update_product(params, mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_list_products_succeeds_without_admin(mock_api):
    # list_products is always available — no context restriction.
    from commerce_mcp.config import CTContext
    ctx = CTContext()  # no admin, no customer
    result = await list_products(ListProductsParams(), mock_api, ctx)
    assert result is not None
    mock_api.get.assert_called_once()
