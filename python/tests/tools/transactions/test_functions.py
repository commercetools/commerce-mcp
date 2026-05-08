import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.transactions.functions import create_transaction, read_transaction
from commerce_mcp.tools.transactions.schemas import (
    ApplicationReference,
    CartReference,
    CreateTransactionParams,
    PaymentIntegrationReference,
    ReadTransactionParams,
    TransactionAmount,
    TransactionItem,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "tx-1", "key": "tx-key"})
    api.post = AsyncMock(return_value={"id": "tx-1", "version": 1})
    return api


def make_create_params() -> CreateTransactionParams:
    return CreateTransactionParams(
        application=ApplicationReference(id="app-1"),
        cart=CartReference(id="cart-1"),
        transactionItems=[
            TransactionItem(
                paymentIntegration=PaymentIntegrationReference(id="pi-1"),
                amount=TransactionAmount(centAmount=1000, currencyCode="EUR"),
            )
        ],
    )


class TestReadTransaction:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_transaction(ReadTransactionParams(id="tx-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/transactions/tx-1", params=None)
        assert json.loads(result)["id"] == "tx-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_transaction(ReadTransactionParams(key="tx-key"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/transactions/key=tx-key", params=None)

    @pytest.mark.asyncio
    async def test_list_transactions(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_transaction(ReadTransactionParams(limit=10), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 10

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_transaction"):
            await read_transaction(ReadTransactionParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError, match="read transaction"):
            await read_transaction(ReadTransactionParams(id="tx-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_transaction(ReadTransactionParams(id="tx-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateTransaction:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        result = await create_transaction(make_create_params(), mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["application"]["id"] == "app-1"
        assert body["cart"]["id"] == "cart-1"
        assert body["transactionItems"][0]["amount"]["centAmount"] == 1000
        assert json.loads(result)["id"] == "tx-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_transaction"):
            await create_transaction(make_create_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError, match="create transaction"):
            await create_transaction(make_create_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await create_transaction(make_create_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
