import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.product_type.functions import (
    create_product_type,
    read_product_type,
    update_product_type,
)
from commerce_mcp.tools.product_type.schemas import (
    AttributeDefinition,
    AttributeType,
    CreateProductTypeParams,
    ProductTypeUpdateAction,
    ReadProductTypeParams,
    UpdateProductTypeParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "pt-1", "key": "t-shirt", "version": 1})
    api.post = AsyncMock(return_value={"id": "pt-1", "version": 2})
    return api


def make_create_params() -> CreateProductTypeParams:
    return CreateProductTypeParams(
        key="t-shirt",
        name="T-Shirt",
        description="A simple t-shirt product type",
        attributes=[
            AttributeDefinition(
                name="color",
                label={"en": "Color"},
                type=AttributeType(name="text"),
            )
        ],
    )


def make_update_params() -> UpdateProductTypeParams:
    return UpdateProductTypeParams(
        id="pt-1",
        version=1,
        actions=[ProductTypeUpdateAction(action="changeName", name="Updated T-Shirt")],
    )


class TestReadProductType:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_product_type(ReadProductTypeParams(id="pt-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/product-types/pt-1", params=None)
        assert json.loads(result)["id"] == "pt-1"

    @pytest.mark.asyncio
    async def test_list(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_product_type(ReadProductTypeParams(limit=5, offset=10), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 5
        assert call_params["offset"] == 10

    @pytest.mark.asyncio
    async def test_list_uses_default_limit_10(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_product_type(ReadProductTypeParams(), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 10

    @pytest.mark.asyncio
    async def test_no_admin_required(self, mock_api):
        # read_product_type has no context guard
        ctx = CTContext()
        result = await read_product_type(ReadProductTypeParams(id="pt-1"), mock_api, ctx)
        mock_api.get.assert_called_once()
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("network error")
        with pytest.raises(SDKError, match="read product type"):
            await read_product_type(ReadProductTypeParams(id="pt-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_product_type(ReadProductTypeParams(id="pt-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateProductType:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        result = await create_product_type(make_create_params(), mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        path = mock_api.post.call_args[0][0]
        assert path == "/product-types"
        body = mock_api.post.call_args[1]["body"]
        assert body["key"] == "t-shirt"
        assert body["name"] == "T-Shirt"
        assert json.loads(result)["id"] == "pt-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_product_type"):
            await create_product_type(make_create_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("server error")
        with pytest.raises(SDKError, match="create product type"):
            await create_product_type(make_create_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await create_product_type(make_create_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestUpdateProductType:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        result = await update_product_type(make_update_params(), mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        path = mock_api.post.call_args[0][0]
        assert path == "/product-types/pt-1"
        body = mock_api.post.call_args[1]["body"]
        assert body["version"] == 1
        assert body["actions"][0]["action"] == "changeName"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="update_product_type"):
            await update_product_type(make_update_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("server error")
        with pytest.raises(SDKError, match="update product type"):
            await update_product_type(make_update_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await update_product_type(make_update_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
