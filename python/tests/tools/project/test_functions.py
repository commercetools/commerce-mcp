import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.project.functions import read_project, update_project
from commerce_mcp.tools.project.schemas import (
    ProjectUpdateAction,
    ReadProjectParams,
    UpdateProjectParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "proj-1", "version": 3, "key": "my-project"})
    api.post = AsyncMock(return_value={"id": "proj-1", "version": 4, "key": "my-project"})
    return api


def make_update_params(version: int | None = 3) -> UpdateProjectParams:
    return UpdateProjectParams(
        version=version,
        actions=[ProjectUpdateAction(action="setName", name="New Name")],
    )


class TestReadProject:
    @pytest.mark.asyncio
    async def test_read_project(self, mock_api, admin_ctx):
        result = await read_project(ReadProjectParams(), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/")
        assert json.loads(result)["key"] == "my-project"

    @pytest.mark.asyncio
    async def test_read_project_no_admin_required(self, mock_api):
        # read_project has no context guard — any context should work
        ctx = CTContext()
        result = await read_project(ReadProjectParams(), mock_api, ctx)
        mock_api.get.assert_called_once_with("/")
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("network error")
        with pytest.raises(SDKError, match="read project"):
            await read_project(ReadProjectParams(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_project(ReadProjectParams(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestUpdateProject:
    @pytest.mark.asyncio
    async def test_update_with_version(self, mock_api, admin_ctx):
        params = make_update_params(version=3)
        result = await update_project(params, mock_api, admin_ctx)
        # Should POST to "/" with version and actions
        mock_api.post.assert_called_once()
        call_kwargs = mock_api.post.call_args
        assert call_kwargs[0][0] == "/"
        body = call_kwargs[1]["body"]
        assert body["version"] == 3
        assert body["actions"][0]["action"] == "setName"
        assert json.loads(result)["version"] == 4

    @pytest.mark.asyncio
    async def test_update_auto_fetches_version_when_none(self, mock_api, admin_ctx):
        params = make_update_params(version=None)
        await update_project(params, mock_api, admin_ctx)
        # GET / is called first to fetch version
        mock_api.get.assert_called_once_with("/")
        # POST / is then called with fetched version
        post_body = mock_api.post.call_args[1]["body"]
        assert post_body["version"] == 3  # returned by mock_api.get

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="update_project"):
            await update_project(make_update_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("server error")
        with pytest.raises(SDKError, match="update project"):
            await update_project(make_update_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await update_project(make_update_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
