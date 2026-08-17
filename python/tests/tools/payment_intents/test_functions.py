import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.payment_intents.functions import update_payment_intents
from commerce_mcp.tools.payment_intents.schemas import PaymentIntentAction, UpdatePaymentIntentsParams


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.post = AsyncMock(return_value={"paymentId": "pay-1", "version": 1})
    return api


def make_update_params():
    return UpdatePaymentIntentsParams(
        paymentId="pay-1",
        actions=[PaymentIntentAction(action="capturePayment")],
    )


class TestUpdatePaymentIntents:
    @pytest.mark.asyncio
    async def test_update(self, mock_api, admin_ctx):
        result = await update_payment_intents(make_update_params(), mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/payments/pay-1/payment-intents",
            body={"actions": [{"action": "capturePayment"}]},
        )
        assert json.loads(result)["paymentId"] == "pay-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="update_payment_intents"):
            await update_payment_intents(make_update_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await update_payment_intents(make_update_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await update_payment_intents(make_update_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
