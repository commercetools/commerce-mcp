from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import ReadProjectParams, UpdateProjectParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_project(
    params: ReadProjectParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        result = await api.get("/")
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read project", e)


async def update_project(
    params: UpdateProjectParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_project", "isAdmin")
    try:
        version = params.version
        if version is None:
            # Auto-fetch current version
            project = await api.get("/")
            version = project["version"]

        actions = [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions]
        body: dict[str, Any] = {
            "version": version,
            "actions": actions,
        }
        result = await api.post("/", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update project", e)
