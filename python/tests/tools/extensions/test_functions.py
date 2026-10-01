import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.extensions.functions import create_extension, read_extension, update_extension
from commerce_mcp.tools.extensions.schemas import (
    CreateExtensionParams,
    ExtensionTrigger,
    ExtensionUpdateAction,
    ReadExtensionParams,
    UpdateExtensionParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "ext-1", "key": "my-ext"})
    api.post = AsyncMock(return_value={"id": "ext-1", "version": 2})
    return api


class TestReadExtension:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_extension(ReadExtensionParams(id="ext-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/extensions/ext-1", params=None)
        assert json.loads(result)["id"] == "ext-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_extension(ReadExtensionParams(key="my-ext"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/extensions/key=my-ext", params=None)

    @pytest.mark.asyncio
    async def test_list_extensions(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_extension(ReadExtensionParams(limit=5), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 5

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_extension"):
            await read_extension(ReadExtensionParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError, match="read extension"):
            await read_extension(ReadExtensionParams(id="ext-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_extension(ReadExtensionParams(id="ext-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateExtension:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreateExtensionParams(
            triggers=[ExtensionTrigger(resourceTypeId="cart", actions=["Create"])],
            destination={"type": "HTTP", "url": "https://example.com/hook"},
        )
        result = await create_extension(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["destination"]["type"] == "HTTP"
        assert json.loads(result)["id"] == "ext-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = CreateExtensionParams(
            triggers=[ExtensionTrigger(resourceTypeId="cart", actions=["Create"])],
            destination={"type": "HTTP", "url": "https://example.com"},
        )
        with pytest.raises(ContextError, match="create_extension"):
            await create_extension(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        params = CreateExtensionParams(
            triggers=[ExtensionTrigger(resourceTypeId="cart", actions=["Create"])],
            destination={"type": "HTTP", "url": "https://example.com"},
        )
        with pytest.raises(SDKError, match="create extension"):
            await create_extension(params, mock_api, admin_ctx)


class TestUpdateExtension:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateExtensionParams(id="ext-1", version=1, actions=[ExtensionUpdateAction(action="setKey", key="new-key")])
        result = await update_extension(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/extensions/ext-1"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateExtensionParams(key="my-ext", version=1, actions=[ExtensionUpdateAction(action="setKey", key="new")])
        await update_extension(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/extensions/key=my-ext"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdateExtensionParams(id="ext-1", version=1, actions=[ExtensionUpdateAction(action="setKey")])
        with pytest.raises(ContextError, match="update_extension"):
            await update_extension(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateExtensionParams(version=1, actions=[ExtensionUpdateAction(action="setKey")])
        with pytest.raises(SDKError):
            await update_extension(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("conflict")
        params = UpdateExtensionParams(id="ext-1", version=1, actions=[ExtensionUpdateAction(action="setKey")])
        with pytest.raises(SDKError, match="update extension"):
            await update_extension(params, mock_api, admin_ctx)
