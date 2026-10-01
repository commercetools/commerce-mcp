import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.zones.functions import create_zone, read_zone, update_zone
from commerce_mcp.tools.zones.schemas import (
    CreateZoneParams,
    ReadZoneParams,
    UpdateZoneParams,
    ZoneUpdateAction,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "zone-1", "name": "Europe"})
    api.post = AsyncMock(return_value={"id": "zone-1", "version": 2})
    return api


# ── read_zone ─────────────────────────────────────────────────────────────────

class TestReadZone:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        params = ReadZoneParams(id="zone-1")
        result = await read_zone(params, mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/zones/zone-1", params=None)
        assert json.loads(result)["id"] == "zone-1"

    @pytest.mark.asyncio
    async def test_read_by_id_with_expand(self, mock_api, admin_ctx):
        params = ReadZoneParams(id="zone-1", expand=["locations"])
        await read_zone(params, mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/zones/zone-1", params={"expand": ["locations"]})

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        params = ReadZoneParams(key="europe")
        result = await read_zone(params, mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/zones/key=europe", params=None)
        assert json.loads(result)["id"] == "zone-1"

    @pytest.mark.asyncio
    async def test_list_zones(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        params = ReadZoneParams(limit=10, offset=0)
        result = await read_zone(params, mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/zones", params={"limit": 10, "offset": 0})
        assert "results" in json.loads(result)

    @pytest.mark.asyncio
    async def test_list_with_where(self, mock_api, admin_ctx):
        params = ReadZoneParams(where=['name="Europe"'])
        await read_zone(params, mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["where"] == ['name="Europe"']

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        ctx = CTContext()
        with pytest.raises(ContextError, match="read_zone"):
            await read_zone(ReadZoneParams(), mock_api, ctx)
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_context_error_with_customer(self, mock_api):
        ctx = CTContext(customer_id="c-1")
        with pytest.raises(ContextError):
            await read_zone(ReadZoneParams(), mock_api, ctx)
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("network error")
        with pytest.raises(SDKError, match="read zone"):
            await read_zone(ReadZoneParams(id="zone-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        params = ReadZoneParams(id="zone-1")
        result = await read_zone(params, mock_api, admin_ctx)
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["id"] == "zone-1"


# ── create_zone ───────────────────────────────────────────────────────────────

class TestCreateZone:
    @pytest.mark.asyncio
    async def test_create_zone(self, mock_api, admin_ctx):
        params = CreateZoneParams(name="Europe", key="europe")
        result = await create_zone(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        call_args = mock_api.post.call_args
        assert call_args[0][0] == "/zones"
        body = call_args[1]["body"]
        assert body["name"] == "Europe"
        assert body["key"] == "europe"
        assert json.loads(result)["id"] == "zone-1"

    @pytest.mark.asyncio
    async def test_create_excludes_none_fields(self, mock_api, admin_ctx):
        params = CreateZoneParams(name="APAC")
        await create_zone(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert "key" not in body
        assert "description" not in body

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        ctx = CTContext()
        with pytest.raises(ContextError, match="create_zone"):
            await create_zone(CreateZoneParams(name="Test"), mock_api, ctx)
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_context_error_with_store(self, mock_api):
        ctx = CTContext(store_key="my-store")
        with pytest.raises(ContextError):
            await create_zone(CreateZoneParams(name="Test"), mock_api, ctx)
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("api error")
        with pytest.raises(SDKError, match="create zone"):
            await create_zone(CreateZoneParams(name="Test"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await create_zone(CreateZoneParams(name="Test"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


# ── update_zone ───────────────────────────────────────────────────────────────

class TestUpdateZone:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateZoneParams(
            id="zone-1",
            version=1,
            actions=[ZoneUpdateAction(action="changeName", name="New Name")],
        )
        result = await update_zone(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        call_args = mock_api.post.call_args
        assert call_args[0][0] == "/zones/zone-1"
        body = call_args[1]["body"]
        assert body["version"] == 1
        assert body["actions"][0]["action"] == "changeName"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateZoneParams(
            key="europe",
            version=2,
            actions=[ZoneUpdateAction(action="setDescription", description="Updated")],
        )
        await update_zone(params, mock_api, admin_ctx)
        call_args = mock_api.post.call_args
        assert call_args[0][0] == "/zones/key=europe"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        ctx = CTContext()
        params = UpdateZoneParams(id="zone-1", version=1, actions=[ZoneUpdateAction(action="changeName", name="X")])
        with pytest.raises(ContextError, match="update_zone"):
            await update_zone(params, mock_api, ctx)
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateZoneParams(version=1, actions=[ZoneUpdateAction(action="changeName", name="X")])
        with pytest.raises(SDKError):
            await update_zone(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("conflict")
        params = UpdateZoneParams(id="zone-1", version=1, actions=[ZoneUpdateAction(action="changeName", name="X")])
        with pytest.raises(SDKError, match="update zone"):
            await update_zone(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        params = UpdateZoneParams(id="zone-1", version=1, actions=[ZoneUpdateAction(action="changeName", name="X")])
        result = await update_zone(params, mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
