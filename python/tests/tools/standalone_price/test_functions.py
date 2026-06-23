import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.standalone_price.functions import (
    create_standalone_price,
    read_standalone_price,
    update_standalone_price,
)
from commerce_mcp.tools.standalone_price.schemas import (
    CreateStandalonePriceParams,
    MoneyValue,
    ReadStandalonePriceParams,
    UpdateStandalonePriceParams,
    StandalonePriceUpdateAction,
)


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "sp-1", "sku": "SKU-1"})
    api.post = AsyncMock(return_value={"id": "sp-1", "version": 1})
    return api


def make_create_params():
    return CreateStandalonePriceParams(
        sku="SKU-1",
        value=MoneyValue(currencyCode="EUR", centAmount=1000),
    )


class TestReadStandalonePrice:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_standalone_price(ReadStandalonePriceParams(id="sp-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/standalone-prices/sp-1", params=None)
        assert json.loads(result)["id"] == "sp-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_standalone_price(ReadStandalonePriceParams(key="sp-key"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/standalone-prices/key=sp-key", params=None)

    @pytest.mark.asyncio
    async def test_list_standalone_prices(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_standalone_price(ReadStandalonePriceParams(limit=10), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 10

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_standalone_price"):
            await read_standalone_price(ReadStandalonePriceParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await read_standalone_price(ReadStandalonePriceParams(id="sp-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_standalone_price(ReadStandalonePriceParams(id="sp-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateStandalonePrice:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        result = await create_standalone_price(make_create_params(), mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["sku"] == "SKU-1"
        assert body["value"]["centAmount"] == 1000
        assert json.loads(result)["id"] == "sp-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_standalone_price"):
            await create_standalone_price(make_create_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await create_standalone_price(make_create_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await create_standalone_price(make_create_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestUpdateStandalonePrice:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateStandalonePriceParams(
            id="sp-1",
            version=1,
            actions=[StandalonePriceUpdateAction(action="changeValue")],
        )
        result = await update_standalone_price(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/standalone-prices/sp-1",
            body={"version": 1, "actions": [{"action": "changeValue"}]},
        )
        assert json.loads(result)["id"] == "sp-1"

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateStandalonePriceParams(
            key="sp-key",
            version=1,
            actions=[StandalonePriceUpdateAction(action="changeValue")],
        )
        await update_standalone_price(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/standalone-prices/key=sp-key",
            body={"version": 1, "actions": [{"action": "changeValue"}]},
        )

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateStandalonePriceParams(
            version=1,
            actions=[StandalonePriceUpdateAction(action="changeValue")],
        )
        with pytest.raises(SDKError):
            await update_standalone_price(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdateStandalonePriceParams(
            id="sp-1",
            version=1,
            actions=[StandalonePriceUpdateAction(action="changeValue")],
        )
        with pytest.raises(ContextError, match="update_standalone_price"):
            await update_standalone_price(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        params = UpdateStandalonePriceParams(
            id="sp-1",
            version=1,
            actions=[StandalonePriceUpdateAction(action="changeValue")],
        )
        with pytest.raises(SDKError):
            await update_standalone_price(params, mock_api, admin_ctx)
