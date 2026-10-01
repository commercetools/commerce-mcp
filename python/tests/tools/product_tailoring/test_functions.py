"""Tests for product_tailoring context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.product_tailoring.functions import (
    read_product_tailoring,
    create_product_tailoring,
    update_product_tailoring,
)
from commerce_mcp.tools.product_tailoring.schemas import (
    ReadProductTailoringParams,
    CreateProductTailoringParams,
    UpdateProductTailoringParams,
    ProductTailoringUpdateAction,
)
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError, ContextError


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "pt-1", "version": 1})
    api.post = AsyncMock(return_value={"id": "pt-1", "version": 2})
    return api


def make_create_params(**kwargs) -> CreateProductTailoringParams:
    return CreateProductTailoringParams(
        key="pt-key-1",
        product_id="prod-1",
        name={"en": "Tailored Name"},
        **kwargs,
    )


def make_update_params(**kwargs) -> UpdateProductTailoringParams:
    return UpdateProductTailoringParams(
        id="pt-1",
        version=1,
        actions=[ProductTailoringUpdateAction(action="setName", name={"en": "New Name"})],
        **kwargs,
    )


# ── Admin context: all three tools ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_product_tailoring_admin_list_uses_product_tailoring_path(mock_api):
    mock_api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "pt-1"}]})
    ctx = CTContext(is_admin=True)
    await read_product_tailoring(ReadProductTailoringParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/product-tailoring"


@pytest.mark.asyncio
async def test_read_product_tailoring_admin_by_id(mock_api):
    ctx = CTContext(is_admin=True)
    await read_product_tailoring(ReadProductTailoringParams(id="pt-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/product-tailoring/pt-1"


@pytest.mark.asyncio
async def test_read_product_tailoring_admin_by_key(mock_api):
    ctx = CTContext(is_admin=True)
    await read_product_tailoring(ReadProductTailoringParams(key="pt-key"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/product-tailoring/key=pt-key"


@pytest.mark.asyncio
async def test_read_product_tailoring_admin_by_product_id_and_store_key(mock_api):
    ctx = CTContext(is_admin=True)
    await read_product_tailoring(
        ReadProductTailoringParams(product_id="prod-1", store_key="eu-store"),
        mock_api,
        ctx,
    )
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/products/prod-1/product-tailoring"


@pytest.mark.asyncio
async def test_read_product_tailoring_admin_by_product_key_and_store_key(mock_api):
    ctx = CTContext(is_admin=True)
    await read_product_tailoring(
        ReadProductTailoringParams(product_key="my-product", store_key="eu-store"),
        mock_api,
        ctx,
    )
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/products/key=my-product/product-tailoring"


@pytest.mark.asyncio
async def test_read_product_tailoring_admin_list_with_where_and_limit(mock_api):
    mock_api.get = AsyncMock(return_value={"count": 0, "results": []})
    ctx = CTContext(is_admin=True)
    await read_product_tailoring(
        ReadProductTailoringParams(where=['product(id="prod-1")'], limit=5, offset=10),
        mock_api,
        ctx,
    )
    path = mock_api.get.call_args[0][0]
    assert path == "/product-tailoring"
    p = mock_api.get.call_args[1]["params"]
    assert p["limit"] == 5
    assert p["offset"] == 10


@pytest.mark.asyncio
async def test_create_product_tailoring_admin_no_store_uses_product_tailoring_path(mock_api):
    ctx = CTContext(is_admin=True)
    await create_product_tailoring(make_create_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/product-tailoring"


@pytest.mark.asyncio
async def test_create_product_tailoring_admin_with_store_key_uses_in_store_path(mock_api):
    ctx = CTContext(is_admin=True)
    await create_product_tailoring(make_create_params(store_key="eu-store"), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/product-tailoring"


@pytest.mark.asyncio
async def test_create_product_tailoring_admin_resolves_product_id_to_reference(mock_api):
    ctx = CTContext(is_admin=True)
    await create_product_tailoring(make_create_params(), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["product"] == {"typeId": "product", "id": "prod-1"}
    # productId should be consumed from body
    assert "productId" not in body


@pytest.mark.asyncio
async def test_create_product_tailoring_admin_resolves_product_key_to_reference(mock_api):
    ctx = CTContext(is_admin=True)
    await create_product_tailoring(
        CreateProductTailoringParams(
            key="pt-key-1",
            product_key="my-product",
            name={"en": "Tailored Name"},
        ),
        mock_api,
        ctx,
    )
    body = mock_api.post.call_args[1]["body"]
    assert body["product"] == {"typeId": "product", "key": "my-product"}
    assert "productKey" not in body


@pytest.mark.asyncio
async def test_update_product_tailoring_admin_by_id(mock_api):
    ctx = CTContext(is_admin=True)
    await update_product_tailoring(make_update_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/product-tailoring/pt-1"


@pytest.mark.asyncio
async def test_update_product_tailoring_admin_by_key(mock_api):
    ctx = CTContext(is_admin=True)
    await update_product_tailoring(
        UpdateProductTailoringParams(
            key="pt-key-1",
            version=1,
            actions=[ProductTailoringUpdateAction(action="setName")],
        ),
        mock_api,
        ctx,
    )
    assert mock_api.post.call_args[0][0] == "/product-tailoring/key=pt-key-1"


@pytest.mark.asyncio
async def test_update_product_tailoring_admin_body_has_version_and_actions(mock_api):
    ctx = CTContext(is_admin=True)
    await update_product_tailoring(make_update_params(), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1
    assert isinstance(body["actions"], list)
    assert body["actions"][0]["action"] == "setName"


@pytest.mark.asyncio
async def test_update_product_tailoring_admin_filters_out_delete_action(mock_api):
    ctx = CTContext(is_admin=True)
    params = UpdateProductTailoringParams(
        id="pt-1",
        version=1,
        actions=[
            ProductTailoringUpdateAction(action="setName"),
            ProductTailoringUpdateAction(action="delete"),
        ],
    )
    await update_product_tailoring(params, mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    action_names = [a["action"] for a in body["actions"]]
    assert "delete" not in action_names
    assert "setName" in action_names


# ── Store context: all three tools ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_product_tailoring_store_list_uses_in_store_path(mock_api):
    mock_api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "pt-1"}]})
    ctx = CTContext(store_key="eu-store")
    await read_product_tailoring(ReadProductTailoringParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/product-tailoring"


@pytest.mark.asyncio
async def test_read_product_tailoring_store_by_id_uses_direct_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await read_product_tailoring(ReadProductTailoringParams(id="pt-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/product-tailoring/pt-1"


@pytest.mark.asyncio
async def test_read_product_tailoring_store_by_key_uses_direct_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await read_product_tailoring(ReadProductTailoringParams(key="pt-key"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/product-tailoring/key=pt-key"


@pytest.mark.asyncio
async def test_read_product_tailoring_store_by_product_id_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await read_product_tailoring(ReadProductTailoringParams(product_id="prod-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/products/prod-1/product-tailoring"


@pytest.mark.asyncio
async def test_read_product_tailoring_store_by_product_key_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await read_product_tailoring(ReadProductTailoringParams(product_key="my-product"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/products/key=my-product/product-tailoring"


@pytest.mark.asyncio
async def test_create_product_tailoring_store_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await create_product_tailoring(make_create_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/product-tailoring"


@pytest.mark.asyncio
async def test_create_product_tailoring_store_injects_store_into_body(mock_api):
    ctx = CTContext(store_key="eu-store")
    await create_product_tailoring(make_create_params(), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["store"] == {"typeId": "store", "key": "eu-store"}


@pytest.mark.asyncio
async def test_create_product_tailoring_store_resolves_product_id_to_reference(mock_api):
    ctx = CTContext(store_key="eu-store")
    await create_product_tailoring(make_create_params(), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["product"] == {"typeId": "product", "id": "prod-1"}
    assert "productId" not in body


@pytest.mark.asyncio
async def test_create_product_tailoring_store_strips_store_key_from_body(mock_api):
    ctx = CTContext(store_key="eu-store")
    await create_product_tailoring(make_create_params(store_key="eu-store"), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert "storeKey" not in body


@pytest.mark.asyncio
async def test_update_product_tailoring_store_by_id(mock_api):
    ctx = CTContext(store_key="eu-store")
    await update_product_tailoring(make_update_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/product-tailoring/pt-1"


@pytest.mark.asyncio
async def test_update_product_tailoring_store_by_key(mock_api):
    ctx = CTContext(store_key="eu-store")
    await update_product_tailoring(
        UpdateProductTailoringParams(
            key="pt-key-1",
            version=1,
            actions=[ProductTailoringUpdateAction(action="setName")],
        ),
        mock_api,
        ctx,
    )
    assert mock_api.post.call_args[0][0] == "/product-tailoring/key=pt-key-1"


@pytest.mark.asyncio
async def test_update_product_tailoring_store_filters_out_delete_action(mock_api):
    ctx = CTContext(store_key="eu-store")
    params = UpdateProductTailoringParams(
        id="pt-1",
        version=1,
        actions=[
            ProductTailoringUpdateAction(action="setName"),
            ProductTailoringUpdateAction(action="delete"),
        ],
    )
    await update_product_tailoring(params, mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    action_names = [a["action"] for a in body["actions"]]
    assert "delete" not in action_names
    assert "setName" in action_names


# ── Customer context: read only ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_product_tailoring_customer_list_uses_product_tailoring_path(mock_api):
    mock_api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "pt-1"}]})
    ctx = CTContext(customer_id="cust-1")
    await read_product_tailoring(ReadProductTailoringParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/product-tailoring"


@pytest.mark.asyncio
async def test_read_product_tailoring_customer_by_id(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await read_product_tailoring(ReadProductTailoringParams(id="pt-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/product-tailoring/pt-1"


@pytest.mark.asyncio
async def test_read_product_tailoring_customer_by_key(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await read_product_tailoring(ReadProductTailoringParams(key="pt-key"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/product-tailoring/key=pt-key"


@pytest.mark.asyncio
async def test_read_product_tailoring_customer_by_product_id_and_store_key(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await read_product_tailoring(
        ReadProductTailoringParams(product_id="prod-1", store_key="eu-store"),
        mock_api,
        ctx,
    )
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/products/prod-1/product-tailoring"


@pytest.mark.asyncio
async def test_create_product_tailoring_raises_context_error_for_customer_context(mock_api):
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="create_product_tailoring"):
        await create_product_tailoring(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_product_tailoring_raises_context_error_for_customer_context(mock_api):
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="update_product_tailoring"):
        await update_product_tailoring(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Empty context: all three tools raise ContextError ─────────────────────────

@pytest.mark.asyncio
async def test_read_product_tailoring_raises_context_error_with_empty_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_product_tailoring"):
        await read_product_tailoring(ReadProductTailoringParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


@pytest.mark.asyncio
async def test_create_product_tailoring_raises_context_error_with_empty_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_product_tailoring"):
        await create_product_tailoring(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_product_tailoring_raises_context_error_with_empty_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_product_tailoring"):
        await update_product_tailoring(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── SDKError on API failure ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_product_tailoring_admin_raises_sdk_error_on_failure(mock_api):
    mock_api.get.side_effect = Exception("500 Server Error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to read product tailoring"):
        await read_product_tailoring(ReadProductTailoringParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_read_product_tailoring_store_raises_sdk_error_on_failure(mock_api):
    mock_api.get.side_effect = Exception("500 Server Error")
    ctx = CTContext(store_key="eu-store")
    with pytest.raises(SDKError, match="Failed to read product tailoring"):
        await read_product_tailoring(ReadProductTailoringParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_read_product_tailoring_customer_raises_sdk_error_on_failure(mock_api):
    mock_api.get.side_effect = Exception("500 Server Error")
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(SDKError, match="Failed to read product tailoring"):
        await read_product_tailoring(ReadProductTailoringParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_product_tailoring_admin_raises_sdk_error_on_failure(mock_api):
    mock_api.post.side_effect = Exception("500 Server Error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to create product tailoring"):
        await create_product_tailoring(make_create_params(), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_product_tailoring_store_raises_sdk_error_on_failure(mock_api):
    mock_api.post.side_effect = Exception("500 Server Error")
    ctx = CTContext(store_key="eu-store")
    with pytest.raises(SDKError, match="Failed to create product tailoring"):
        await create_product_tailoring(make_create_params(), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_product_tailoring_admin_raises_sdk_error_on_failure(mock_api):
    mock_api.post.side_effect = Exception("500 Server Error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to update product tailoring"):
        await update_product_tailoring(make_update_params(), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_product_tailoring_store_raises_sdk_error_on_failure(mock_api):
    mock_api.post.side_effect = Exception("500 Server Error")
    ctx = CTContext(store_key="eu-store")
    with pytest.raises(SDKError, match="Failed to update product tailoring"):
        await update_product_tailoring(make_update_params(), mock_api, ctx)
