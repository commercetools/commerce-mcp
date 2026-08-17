import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.payment_methods.functions import (
    create_payment_methods,
    read_payment_methods,
    update_payment_methods,
)
from commerce_mcp.tools.payment_methods.schemas import (
    CreatePaymentMethodsParams,
    PaymentMethodUpdateAction,
    ReadPaymentMethodsParams,
    UpdatePaymentMethodsParams,
)


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "pm-1", "key": "pm-key"})
    api.post = AsyncMock(return_value={"id": "pm-1", "version": 1})
    return api


class TestReadPaymentMethods:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_payment_methods(ReadPaymentMethodsParams(id="pm-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/payment-methods/pm-1", params=None)
        assert json.loads(result)["id"] == "pm-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_payment_methods(ReadPaymentMethodsParams(key="pm-key"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/payment-methods/key=pm-key", params=None)

    @pytest.mark.asyncio
    async def test_list_payment_methods(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_payment_methods(ReadPaymentMethodsParams(limit=10), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 10

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_payment_methods"):
            await read_payment_methods(ReadPaymentMethodsParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await read_payment_methods(ReadPaymentMethodsParams(id="pm-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_payment_methods(ReadPaymentMethodsParams(id="pm-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreatePaymentMethods:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreatePaymentMethodsParams(name={"en": "Card"})
        result = await create_payment_methods(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["name"] == {"en": "Card"}
        assert json.loads(result)["id"] == "pm-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_payment_methods"):
            await create_payment_methods(CreatePaymentMethodsParams(name={"en": "Card"}), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await create_payment_methods(CreatePaymentMethodsParams(name={"en": "Card"}), mock_api, admin_ctx)


class TestUpdatePaymentMethods:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdatePaymentMethodsParams(
            id="pm-1",
            version=1,
            actions=[PaymentMethodUpdateAction(action="setName")],
        )
        result = await update_payment_methods(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/payment-methods/pm-1",
            body={"version": 1, "actions": [{"action": "setName"}]},
        )
        assert json.loads(result)["id"] == "pm-1"

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdatePaymentMethodsParams(
            key="pm-key",
            version=1,
            actions=[PaymentMethodUpdateAction(action="setName")],
        )
        await update_payment_methods(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/payment-methods/key=pm-key",
            body={"version": 1, "actions": [{"action": "setName"}]},
        )

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdatePaymentMethodsParams(
            version=1,
            actions=[PaymentMethodUpdateAction(action="setName")],
        )
        with pytest.raises(SDKError):
            await update_payment_methods(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdatePaymentMethodsParams(
            id="pm-1",
            version=1,
            actions=[PaymentMethodUpdateAction(action="setName")],
        )
        with pytest.raises(ContextError, match="update_payment_methods"):
            await update_payment_methods(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        params = UpdatePaymentMethodsParams(
            id="pm-1",
            version=1,
            actions=[PaymentMethodUpdateAction(action="setName")],
        )
        with pytest.raises(SDKError):
            await update_payment_methods(params, mock_api, admin_ctx)
