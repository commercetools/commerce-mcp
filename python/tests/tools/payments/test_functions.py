import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.payments.functions import create_payments, read_payments, update_payments
from commerce_mcp.tools.payments.schemas import (
    CreatePaymentsParams,
    PaymentUpdateAction,
    ReadPaymentsParams,
    UpdatePaymentsParams,
)


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "pay-1", "key": "pay-key"})
    api.post = AsyncMock(return_value={"id": "pay-1", "version": 1})
    return api


class TestReadPayments:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_payments(ReadPaymentsParams(id="pay-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/payments/pay-1", params=None)
        assert json.loads(result)["id"] == "pay-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_payments(ReadPaymentsParams(key="pay-key"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/payments/key=pay-key", params=None)

    @pytest.mark.asyncio
    async def test_list_payments(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_payments(ReadPaymentsParams(limit=10), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 10

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_payments"):
            await read_payments(ReadPaymentsParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await read_payments(ReadPaymentsParams(id="pay-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_payments(ReadPaymentsParams(id="pay-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreatePayments:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreatePaymentsParams(
            amount_planned={"currencyCode": "EUR", "centAmount": 1000, "type": "centPrecision"},
        )
        result = await create_payments(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        assert json.loads(result)["id"] == "pay-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = CreatePaymentsParams(
            amount_planned={"currencyCode": "EUR", "centAmount": 1000, "type": "centPrecision"},
        )
        with pytest.raises(ContextError, match="create_payments"):
            await create_payments(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        params = CreatePaymentsParams(
            amount_planned={"currencyCode": "EUR", "centAmount": 1000, "type": "centPrecision"},
        )
        with pytest.raises(SDKError):
            await create_payments(params, mock_api, admin_ctx)


class TestUpdatePayments:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdatePaymentsParams(
            id="pay-1",
            version=1,
            actions=[PaymentUpdateAction(action="addTransaction")],
        )
        result = await update_payments(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/payments/pay-1",
            body={"version": 1, "actions": [{"action": "addTransaction"}]},
        )
        assert json.loads(result)["id"] == "pay-1"

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdatePaymentsParams(
            key="pay-key",
            version=1,
            actions=[PaymentUpdateAction(action="addTransaction")],
        )
        await update_payments(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/payments/key=pay-key",
            body={"version": 1, "actions": [{"action": "addTransaction"}]},
        )

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdatePaymentsParams(
            version=1,
            actions=[PaymentUpdateAction(action="addTransaction")],
        )
        with pytest.raises(SDKError):
            await update_payments(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdatePaymentsParams(
            id="pay-1",
            version=1,
            actions=[PaymentUpdateAction(action="addTransaction")],
        )
        with pytest.raises(ContextError, match="update_payments"):
            await update_payments(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        params = UpdatePaymentsParams(
            id="pay-1",
            version=1,
            actions=[PaymentUpdateAction(action="addTransaction")],
        )
        with pytest.raises(SDKError):
            await update_payments(params, mock_api, admin_ctx)
