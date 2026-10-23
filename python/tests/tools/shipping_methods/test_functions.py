import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.shipping_methods.functions import (
    create_shipping_methods,
    read_shipping_methods,
    update_shipping_methods,
)
from commerce_mcp.tools.shipping_methods.schemas import (
    CreateShippingMethodsParams,
    MoneyDraft,
    ReadShippingMethodsParams,
    ShippingMethodUpdateAction,
    ShippingRate,
    UpdateShippingMethodsParams,
    ZoneRate,
    ZoneReference,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "sm-1", "key": "standard-shipping", "version": 1})
    api.post = AsyncMock(return_value={"id": "sm-1", "version": 2})
    return api


def make_create_params() -> CreateShippingMethodsParams:
    return CreateShippingMethodsParams(
        name="Standard Shipping",
        zoneRates=[
            ZoneRate(
                zone=ZoneReference(id="zone-1", typeId="zone"),
                shippingRates=[
                    ShippingRate(
                        price=MoneyDraft(
                            type="centPrecision",
                            currencyCode="EUR",
                            centAmount=500,
                            fractionDigits=2,
                        )
                    )
                ],
            )
        ],
    )


def make_update_params(use_id: bool = True) -> UpdateShippingMethodsParams:
    return UpdateShippingMethodsParams(
        version=1,
        actions=[ShippingMethodUpdateAction(action="changeName", name="Express Shipping")],
        id="sm-1" if use_id else None,
        key="standard-shipping" if not use_id else None,
    )


class TestReadShippingMethods:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_shipping_methods(
            ReadShippingMethodsParams(id="sm-1"), mock_api, admin_ctx
        )
        mock_api.get.assert_called_once_with("/shipping-methods/sm-1", params=None)
        assert json.loads(result)["id"] == "sm-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_shipping_methods(
            ReadShippingMethodsParams(key="standard-shipping"), mock_api, admin_ctx
        )
        mock_api.get.assert_called_once_with(
            "/shipping-methods/key=standard-shipping", params=None
        )

    @pytest.mark.asyncio
    async def test_list(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_shipping_methods(
            ReadShippingMethodsParams(limit=20, offset=40), mock_api, admin_ctx
        )
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 20
        assert call_params["offset"] == 40

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_shipping_methods"):
            await read_shipping_methods(ReadShippingMethodsParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("network error")
        with pytest.raises(SDKError, match="read shipping methods"):
            await read_shipping_methods(
                ReadShippingMethodsParams(id="sm-1"), mock_api, admin_ctx
            )

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_shipping_methods(
            ReadShippingMethodsParams(id="sm-1"), mock_api, admin_ctx
        )
        assert isinstance(result, str)
        json.loads(result)


class TestCreateShippingMethods:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        result = await create_shipping_methods(make_create_params(), mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        path = mock_api.post.call_args[0][0]
        assert path == "/shipping-methods"
        body = mock_api.post.call_args[1]["body"]
        assert body["name"] == "Standard Shipping"
        assert json.loads(result)["id"] == "sm-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_shipping_methods"):
            await create_shipping_methods(make_create_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("server error")
        with pytest.raises(SDKError, match="create shipping methods"):
            await create_shipping_methods(make_create_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await create_shipping_methods(make_create_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestUpdateShippingMethods:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        result = await update_shipping_methods(make_update_params(use_id=True), mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        path = mock_api.post.call_args[0][0]
        assert path == "/shipping-methods/sm-1"
        body = mock_api.post.call_args[1]["body"]
        assert body["version"] == 1
        assert body["actions"][0]["action"] == "changeName"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        await update_shipping_methods(make_update_params(use_id=False), mock_api, admin_ctx)
        path = mock_api.post.call_args[0][0]
        assert path == "/shipping-methods/key=standard-shipping"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="update_shipping_methods"):
            await update_shipping_methods(make_update_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateShippingMethodsParams(
            version=1,
            actions=[ShippingMethodUpdateAction(action="changeName", name="X")],
        )
        with pytest.raises(SDKError, match="update shipping methods"):
            await update_shipping_methods(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("server error")
        with pytest.raises(SDKError, match="update shipping methods"):
            await update_shipping_methods(make_update_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await update_shipping_methods(make_update_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
