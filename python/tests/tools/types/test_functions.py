import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.types.functions import create_type, read_type, update_type
from commerce_mcp.tools.types.schemas import (
    CreateTypeParams,
    ReadTypeParams,
    TypeUpdateAction,
    UpdateTypeParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "type-1", "key": "my-type"})
    api.post = AsyncMock(return_value={"id": "type-1", "version": 2})
    return api


# ── read_type ─────────────────────────────────────────────────────────────────

class TestReadType:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        params = ReadTypeParams(id="type-1")
        result = await read_type(params, mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/types/type-1", params=None)
        assert json.loads(result)["id"] == "type-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        params = ReadTypeParams(key="my-type")
        await read_type(params, mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/types/key=my-type", params=None)

    @pytest.mark.asyncio
    async def test_list_types(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        params = ReadTypeParams(limit=10, offset=0)
        result = await read_type(params, mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 10
        assert call_params["offset"] == 0
        assert "results" in json.loads(result)

    @pytest.mark.asyncio
    async def test_list_with_where(self, mock_api, admin_ctx):
        params = ReadTypeParams(where=['key="my-type"'])
        await read_type(params, mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["where"] == ['key="my-type"']

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        ctx = CTContext()
        with pytest.raises(ContextError, match="read_type"):
            await read_type(ReadTypeParams(), mock_api, ctx)
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("network error")
        with pytest.raises(SDKError, match="read type"):
            await read_type(ReadTypeParams(id="type-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_type(ReadTypeParams(id="type-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


# ── create_type ───────────────────────────────────────────────────────────────

class TestCreateType:
    @pytest.mark.asyncio
    async def test_create_type(self, mock_api, admin_ctx):
        params = CreateTypeParams(
            key="my-type",
            name="My Type",
            resourceTypeIds=["category"],
        )
        result = await create_type(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        body = mock_api.post.call_args[1]["body"]
        assert body["key"] == "my-type"
        assert body["name"] == "My Type"
        assert body["resourceTypeIds"] == ["category"]
        assert json.loads(result)["id"] == "type-1"

    @pytest.mark.asyncio
    async def test_create_excludes_none_fields(self, mock_api, admin_ctx):
        params = CreateTypeParams(key="t", name="T", resourceTypeIds=["product"])
        await create_type(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert "description" not in body
        assert "fieldDefinitions" not in body

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        ctx = CTContext()
        with pytest.raises(ContextError, match="create_type"):
            await create_type(CreateTypeParams(key="t", name="T", resourceTypeIds=["product"]), mock_api, ctx)
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("validation error")
        with pytest.raises(SDKError, match="create type"):
            await create_type(CreateTypeParams(key="t", name="T", resourceTypeIds=["product"]), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await create_type(CreateTypeParams(key="t", name="T", resourceTypeIds=["product"]), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


# ── update_type ───────────────────────────────────────────────────────────────

class TestUpdateType:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateTypeParams(
            id="type-1",
            version=1,
            actions=[TypeUpdateAction(action="changeName", name="New Name")],
        )
        result = await update_type(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/types/type-1"
        body = mock_api.post.call_args[1]["body"]
        assert body["version"] == 1
        assert body["actions"][0]["action"] == "changeName"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateTypeParams(
            key="my-type",
            version=1,
            actions=[TypeUpdateAction(action="setDescription", description="Updated")],
        )
        await update_type(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/types/key=my-type"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        ctx = CTContext()
        params = UpdateTypeParams(id="type-1", version=1, actions=[TypeUpdateAction(action="changeName")])
        with pytest.raises(ContextError, match="update_type"):
            await update_type(params, mock_api, ctx)
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateTypeParams(version=1, actions=[TypeUpdateAction(action="changeName")])
        with pytest.raises(SDKError):
            await update_type(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("conflict")
        params = UpdateTypeParams(id="type-1", version=1, actions=[TypeUpdateAction(action="changeName")])
        with pytest.raises(SDKError, match="update type"):
            await update_type(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        params = UpdateTypeParams(id="type-1", version=1, actions=[TypeUpdateAction(action="changeName")])
        result = await update_type(params, mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
