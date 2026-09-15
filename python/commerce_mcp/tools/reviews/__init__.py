from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_review, read_review, update_review
from .schemas import CreateReviewParams, ReadReviewParams, UpdateReviewParams
from .prompts import CREATE_REVIEW_PROMPT, READ_REVIEW_PROMPT, UPDATE_REVIEW_PROMPT

_REVIEWS_TOOLS = [
    ToolDefinition(
        method="read_review",
        name="Read Review",
        description=READ_REVIEW_PROMPT,
        parameters=ReadReviewParams,
        handler=read_review,
        actions={"review": {"read": True}},
    ),
    ToolDefinition(
        method="create_review",
        name="Create Review",
        description=CREATE_REVIEW_PROMPT,
        parameters=CreateReviewParams,
        handler=create_review,
        actions={"review": {"create": True}},
    ),
    ToolDefinition(
        method="update_review",
        name="Update Review",
        description=UPDATE_REVIEW_PROMPT,
        parameters=UpdateReviewParams,
        handler=update_review,
        actions={"review": {"update": True}},
    ),
]

for _tool in _REVIEWS_TOOLS:
    register_tool(_tool)
