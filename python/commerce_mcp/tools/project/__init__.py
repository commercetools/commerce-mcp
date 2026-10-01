from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import read_project, update_project
from .schemas import ReadProjectParams, UpdateProjectParams
from .prompts import READ_PROJECT_PROMPT, UPDATE_PROJECT_PROMPT

_PROJECT_TOOLS = [
    ToolDefinition(
        method="read_project",
        name="Read Project",
        description=READ_PROJECT_PROMPT,
        parameters=ReadProjectParams,
        handler=read_project,
        actions={"project": {"read": True}},
    ),
    ToolDefinition(
        method="update_project",
        name="Update Project",
        description=UPDATE_PROJECT_PROMPT,
        parameters=UpdateProjectParams,
        handler=update_project,
        actions={"project": {"update": True}},
    ),
]

for _tool in _PROJECT_TOOLS:
    register_tool(_tool)
