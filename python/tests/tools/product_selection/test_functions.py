import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.product_selection.functions import (
    create_product_selection,
    read_product_selection,
    update_product_selection,
)
from commerce_mcp.tools.product_selection.schemas import (
    CreateProductSelectionParams,
    ProductSelectionUpdateAction,
    ReadProductSelectionParams,
    UpdateProductSelectionParams,
)


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "ps-1", "key": "ps-key"})
    api.post = AsyncMock(return_value={"id": "ps-1", "version": 1})
    return api


class TestReadProductSelection:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_product_selection(ReadProductSelectionParams(id="ps-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/product-selections/ps-1", params=None)
        assert json.loads(result)["id"] == "ps-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_product_selection(ReadProductSelectionParams(key="ps-key"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/product-selections/key=ps-key", params=None)

    @pytest.mark.asyncio
    async def test_list_product_selections(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_product_selection(ReadProductSelectionParams(limit=5), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 5

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_product_selection"):
            await read_product_selection(ReadProductSelectionParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await read_product_selection(ReadProductSelectionParams(id="ps-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_product_selection(ReadProductSelectionParams(id="ps-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateProductSelection:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreateProductSelectionParams(name={"en": "Featured Products"})
        result = await create_product_selection(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["name"] == {"en": "Featured Products"}
        assert json.loads(result)["id"] == "ps-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_product_selection"):
            await create_product_selection(
                CreateProductSelectionParams(name={"en": "Featured Products"}),
                mock_api,
                CTContext(),
            )
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await create_product_selection(
                CreateProductSelectionParams(name={"en": "Featured Products"}),
                mock_api,
                admin_ctx,
            )


class TestUpdateProductSelection:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateProductSelectionParams(
            id="ps-1",
            version=1,
            actions=[ProductSelectionUpdateAction(action="addProduct")],
        )
        result = await update_product_selection(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/product-selections/ps-1",
            body={"version": 1, "actions": [{"action": "addProduct"}]},
        )
        assert json.loads(result)["id"] == "ps-1"

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateProductSelectionParams(
            key="ps-key",
            version=1,
            actions=[ProductSelectionUpdateAction(action="addProduct")],
        )
        await update_product_selection(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/product-selections/key=ps-key",
            body={"version": 1, "actions": [{"action": "addProduct"}]},
        )

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateProductSelectionParams(
            version=1,
            actions=[ProductSelectionUpdateAction(action="addProduct")],
        )
        with pytest.raises(SDKError):
            await update_product_selection(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdateProductSelectionParams(
            id="ps-1",
            version=1,
            actions=[ProductSelectionUpdateAction(action="addProduct")],
        )
        with pytest.raises(ContextError, match="update_product_selection"):
            await update_product_selection(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        params = UpdateProductSelectionParams(
            id="ps-1",
            version=1,
            actions=[ProductSelectionUpdateAction(action="addProduct")],
        )
        with pytest.raises(SDKError):
            await update_product_selection(params, mock_api, admin_ctx)
