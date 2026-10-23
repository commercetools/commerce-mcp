import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.channel.functions import create_channel, read_channel, update_channel
from commerce_mcp.tools.channel.schemas import (
    ChannelUpdateAction,
    CreateChannelParams,
    ReadChannelParams,
    UpdateChannelParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "ch-1", "key": "warehouse-1"})
    api.post = AsyncMock(return_value={"id": "ch-1", "version": 2})
    return api


# ── read_channel ──────────────────────────────────────────────────────────────

class TestReadChannel:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        params = ReadChannelParams(id="ch-1")
        result = await read_channel(params, mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/channels/ch-1", params=None)
        assert json.loads(result)["id"] == "ch-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        params = ReadChannelParams(key="warehouse-1")
        await read_channel(params, mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/channels/key=warehouse-1", params=None)

    @pytest.mark.asyncio
    async def test_list_channels_default_limit(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        params = ReadChannelParams()
        await read_channel(params, mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 20

    @pytest.mark.asyncio
    async def test_list_channels_with_where(self, mock_api, admin_ctx):
        params = ReadChannelParams(where=['roles contains any "InventorySupply"'], limit=5)
        await read_channel(params, mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 5
        assert call_params["where"] == ['roles contains any "InventorySupply"']

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        ctx = CTContext()
        with pytest.raises(ContextError, match="read_channel"):
            await read_channel(ReadChannelParams(), mock_api, ctx)
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_context_error_with_customer(self, mock_api):
        ctx = CTContext(customer_id="c-1")
        with pytest.raises(ContextError):
            await read_channel(ReadChannelParams(), mock_api, ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("network error")
        with pytest.raises(SDKError, match="read channel"):
            await read_channel(ReadChannelParams(id="ch-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_channel(ReadChannelParams(id="ch-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


# ── create_channel ────────────────────────────────────────────────────────────

class TestCreateChannel:
    @pytest.mark.asyncio
    async def test_create_channel(self, mock_api, admin_ctx):
        params = CreateChannelParams(key="warehouse-1", roles=["InventorySupply"])
        result = await create_channel(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        body = mock_api.post.call_args[1]["body"]
        assert body["key"] == "warehouse-1"
        assert body["roles"] == ["InventorySupply"]
        assert json.loads(result)["id"] == "ch-1"

    @pytest.mark.asyncio
    async def test_create_excludes_none_fields(self, mock_api, admin_ctx):
        params = CreateChannelParams(key="dist", roles=["ProductDistribution"])
        await create_channel(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert "name" not in body
        assert "description" not in body

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        ctx = CTContext()
        with pytest.raises(ContextError, match="create_channel"):
            await create_channel(CreateChannelParams(key="x", roles=["Primary"]), mock_api, ctx)
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("validation error")
        with pytest.raises(SDKError, match="create channel"):
            await create_channel(CreateChannelParams(key="x", roles=["Primary"]), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await create_channel(CreateChannelParams(key="x", roles=["Primary"]), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


# ── update_channel ────────────────────────────────────────────────────────────

class TestUpdateChannel:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateChannelParams(
            id="ch-1",
            version=1,
            actions=[ChannelUpdateAction(action="setRoles", roles=["OrderExport"])],
        )
        result = await update_channel(params, mock_api, admin_ctx)
        call_args = mock_api.post.call_args
        assert call_args[0][0] == "/channels/ch-1"
        body = call_args[1]["body"]
        assert body["version"] == 1
        assert body["actions"][0]["action"] == "setRoles"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateChannelParams(
            key="warehouse-1",
            version=1,
            actions=[ChannelUpdateAction(action="changeName", name={"en": "New Name"})],
        )
        await update_channel(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/channels/key=warehouse-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        ctx = CTContext()
        params = UpdateChannelParams(id="ch-1", version=1, actions=[ChannelUpdateAction(action="changeName")])
        with pytest.raises(ContextError, match="update_channel"):
            await update_channel(params, mock_api, ctx)
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateChannelParams(version=1, actions=[ChannelUpdateAction(action="changeName")])
        with pytest.raises(SDKError):
            await update_channel(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("conflict")
        params = UpdateChannelParams(id="ch-1", version=1, actions=[ChannelUpdateAction(action="changeName")])
        with pytest.raises(SDKError, match="update channel"):
            await update_channel(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        params = UpdateChannelParams(id="ch-1", version=1, actions=[ChannelUpdateAction(action="changeName")])
        result = await update_channel(params, mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
