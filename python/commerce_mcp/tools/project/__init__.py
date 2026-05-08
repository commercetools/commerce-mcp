from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import read_project, update_project
from .schemas import ReadProjectParams, UpdateProjectParams

_PROJECT_TOOLS = [
    ToolDefinition(
        method="read_project",
        name="Read Project",
        description=(
            "Read information about a commercetools project, including countries, currencies, "
            "languages, and feature configurations. If no projectKey is provided, the current "
            "project is used."
        ),
        parameters=ReadProjectParams,
        handler=read_project,
        actions={"project": {"read": True}},
    ),
    ToolDefinition(
        method="update_project",
        name="Update Project",
        description=(
            "Update settings for a commercetools project. This is an admin-only operation. "
            "Provide a list of update actions such as changeName, changeCountries, changeCurrencies, "
            "changeLanguages, changeMessagesConfiguration, and more. If version is omitted, the "
            "current version is fetched automatically."
        ),
        parameters=UpdateProjectParams,
        handler=update_project,
        actions={"project": {"update": True}},
    ),
]

for _tool in _PROJECT_TOOLS:
    register_tool(_tool)
