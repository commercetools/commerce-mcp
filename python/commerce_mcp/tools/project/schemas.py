from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class ReadProjectParams(BaseModel):
    project_key: str | None = Field(
        None,
        description="The key of the project to read. If not provided, the current project will be used.",
    )


class ProjectUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateProjectParams(BaseModel):
    version: int | None = Field(
        None,
        description=(
            "The current version of the project. "
            "If not provided, the current version will be fetched automatically."
        ),
    )
    actions: list[ProjectUpdateAction] = Field(
        description="The list of update actions to apply to the project."
    )
    project_key: str | None = Field(
        None,
        description="The key of the project to update. If not provided, the current project will be used.",
    )
