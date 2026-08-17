import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.product_discount.functions import (
    create_product_discount,
    read_product_discount,
    update_product_discount,
)
from commerce_mcp.tools.product_discount.schemas import (
    CreateProductDiscountParams,
    ProductDiscountUpdateAction,
    ReadProductDiscountParams,
    UpdateProductDiscountParams,
)


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "pd-1", "key": "pd-key"})
    api.post = AsyncMock(return_value={"id": "pd-1", "version": 1})
    return api


def make_create_params():
    return CreateProductDiscountParams(
        name={"en": "10% off"},
        value={"type": "relative", "permyriad": 1000},
        predicate="true",
        sortOrder="0.5",
    )


class TestReadProductDiscount:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_product_discount(ReadProductDiscountParams(id="pd-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/product-discounts/pd-1", params=None)
        assert json.loads(result)["id"] == "pd-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_product_discount(ReadProductDiscountParams(key="pd-key"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/product-discounts/key=pd-key", params=None)

    @pytest.mark.asyncio
    async def test_list_product_discounts(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_product_discount(ReadProductDiscountParams(limit=5), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 5

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_product_discount"):
            await read_product_discount(ReadProductDiscountParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await read_product_discount(ReadProductDiscountParams(id="pd-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_product_discount(ReadProductDiscountParams(id="pd-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateProductDiscount:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        result = await create_product_discount(make_create_params(), mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["name"] == {"en": "10% off"}
        assert body["predicate"] == "true"
        assert json.loads(result)["id"] == "pd-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_product_discount"):
            await create_product_discount(make_create_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await create_product_discount(make_create_params(), mock_api, admin_ctx)


class TestUpdateProductDiscount:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateProductDiscountParams(
            id="pd-1",
            version=1,
            actions=[ProductDiscountUpdateAction(action="changeIsActive")],
        )
        result = await update_product_discount(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/product-discounts/pd-1",
            body={"version": 1, "actions": [{"action": "changeIsActive"}]},
        )
        assert json.loads(result)["id"] == "pd-1"

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateProductDiscountParams(
            key="pd-key",
            version=1,
            actions=[ProductDiscountUpdateAction(action="changeIsActive")],
        )
        await update_product_discount(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/product-discounts/key=pd-key",
            body={"version": 1, "actions": [{"action": "changeIsActive"}]},
        )

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateProductDiscountParams(
            version=1,
            actions=[ProductDiscountUpdateAction(action="changeIsActive")],
        )
        with pytest.raises(SDKError):
            await update_product_discount(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdateProductDiscountParams(
            id="pd-1",
            version=1,
            actions=[ProductDiscountUpdateAction(action="changeIsActive")],
        )
        with pytest.raises(ContextError, match="update_product_discount"):
            await update_product_discount(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        params = UpdateProductDiscountParams(
            id="pd-1",
            version=1,
            actions=[ProductDiscountUpdateAction(action="changeIsActive")],
        )
        with pytest.raises(SDKError):
            await update_product_discount(params, mock_api, admin_ctx)
