import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.custom_objects.functions import (
    create_custom_object,
    read_custom_object,
    update_custom_object,
)
from commerce_mcp.tools.custom_objects.schemas import (
    CreateCustomObjectParams,
    ReadCustomObjectParams,
    UpdateCustomObjectParams,
)


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"container": "my-app", "key": "setting-1", "value": {"foo": "bar"}})
    api.post = AsyncMock(return_value={"container": "my-app", "key": "setting-1", "version": 1})
    return api


class TestReadCustomObject:
    @pytest.mark.asyncio
    async def test_read_by_container_and_key(self, mock_api, admin_ctx):
        result = await read_custom_object(
            ReadCustomObjectParams(container="my-app", key="setting-1"), mock_api, admin_ctx
        )
        mock_api.get.assert_called_once_with("/custom-objects/my-app/setting-1")
        assert json.loads(result)["container"] == "my-app"

    @pytest.mark.asyncio
    async def test_read_by_container(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_custom_object(ReadCustomObjectParams(container="my-app"), mock_api, admin_ctx)
        call_args = mock_api.get.call_args
        assert call_args[0][0] == "/custom-objects/my-app"

    @pytest.mark.asyncio
    async def test_list_all_custom_objects(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_custom_object(ReadCustomObjectParams(limit=10), mock_api, admin_ctx)
        call_args = mock_api.get.call_args
        assert call_args[0][0] == "/custom-objects"
        assert call_args[1]["params"]["limit"] == 10

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_custom_object"):
            await read_custom_object(ReadCustomObjectParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await read_custom_object(ReadCustomObjectParams(container="my-app", key="k1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_custom_object(
            ReadCustomObjectParams(container="my-app", key="setting-1"), mock_api, admin_ctx
        )
        assert isinstance(result, str)
        json.loads(result)


class TestCreateCustomObject:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreateCustomObjectParams(container="my-app", key="setting-1", value={"foo": "bar"})
        result = await create_custom_object(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["container"] == "my-app"
        assert body["key"] == "setting-1"
        assert body["value"] == {"foo": "bar"}
        assert json.loads(result)["container"] == "my-app"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_custom_object"):
            await create_custom_object(
                CreateCustomObjectParams(container="my-app", key="k1", value={}),
                mock_api,
                CTContext(),
            )
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await create_custom_object(
                CreateCustomObjectParams(container="my-app", key="k1", value={}),
                mock_api,
                admin_ctx,
            )


class TestUpdateCustomObject:
    @pytest.mark.asyncio
    async def test_update(self, mock_api, admin_ctx):
        params = UpdateCustomObjectParams(container="my-app", key="setting-1", value={"foo": "updated"})
        result = await update_custom_object(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["container"] == "my-app"
        assert body["key"] == "setting-1"
        assert body["value"] == {"foo": "updated"}
        assert json.loads(result)["container"] == "my-app"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="update_custom_object"):
            await update_custom_object(
                UpdateCustomObjectParams(container="my-app", key="k1", value={}),
                mock_api,
                CTContext(),
            )
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await update_custom_object(
                UpdateCustomObjectParams(container="my-app", key="k1", value={}),
                mock_api,
                admin_ctx,
            )
