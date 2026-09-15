import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.subscriptions.functions import create_subscription, read_subscription, update_subscription
from commerce_mcp.tools.subscriptions.schemas import (
    CreateSubscriptionParams,
    ReadSubscriptionParams,
    SubscriptionUpdateAction,
    UpdateSubscriptionParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "sub-1", "key": "my-sub"})
    api.post = AsyncMock(return_value={"id": "sub-1", "version": 2})
    return api


class TestReadSubscription:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_subscription(ReadSubscriptionParams(id="sub-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with(f"/subscriptions/sub-1")
        assert json.loads(result)["id"] == "sub-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_subscription(ReadSubscriptionParams(key="my-sub"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/subscriptions/key=my-sub")

    @pytest.mark.asyncio
    async def test_list_subscriptions(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_subscription(ReadSubscriptionParams(limit=5), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 5

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_subscription"):
            await read_subscription(ReadSubscriptionParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError, match="read subscription"):
            await read_subscription(ReadSubscriptionParams(id="sub-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_subscription(ReadSubscriptionParams(id="sub-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateSubscription:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreateSubscriptionParams(destination={"type": "SQS", "queueUrl": "https://sqs.example.com/q", "region": "us-east-1"})
        result = await create_subscription(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["destination"]["type"] == "SQS"
        assert json.loads(result)["id"] == "sub-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = CreateSubscriptionParams(destination={"type": "SNS", "topicArn": "arn:aws:sns:us-east-1:123:topic"})
        with pytest.raises(ContextError, match="create_subscription"):
            await create_subscription(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError, match="create subscription"):
            await create_subscription(
                CreateSubscriptionParams(destination={"type": "SQS", "queueUrl": "https://q", "region": "us-east-1"}),
                mock_api, admin_ctx,
            )


class TestUpdateSubscription:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateSubscriptionParams(id="sub-1", version=1, actions=[SubscriptionUpdateAction(action="setKey", key="new")])
        result = await update_subscription(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/subscriptions/sub-1"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateSubscriptionParams(key="my-sub", version=1, actions=[SubscriptionUpdateAction(action="setKey", key="new")])
        await update_subscription(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/subscriptions/key=my-sub"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdateSubscriptionParams(id="sub-1", version=1, actions=[SubscriptionUpdateAction(action="setKey")])
        with pytest.raises(ContextError, match="update_subscription"):
            await update_subscription(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateSubscriptionParams(version=1, actions=[SubscriptionUpdateAction(action="setKey")])
        with pytest.raises(SDKError):
            await update_subscription(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("conflict")
        params = UpdateSubscriptionParams(id="sub-1", version=1, actions=[SubscriptionUpdateAction(action="setKey")])
        with pytest.raises(SDKError, match="update subscription"):
            await update_subscription(params, mock_api, admin_ctx)
