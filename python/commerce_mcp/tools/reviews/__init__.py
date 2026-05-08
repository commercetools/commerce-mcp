from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_review, read_review, update_review
from .schemas import CreateReviewParams, ReadReviewParams, UpdateReviewParams

_REVIEWS_TOOLS = [
    ToolDefinition(
        method="read_review",
        name="Read Review",
        description="Read or list reviews. Provide an id or key to fetch a specific review, or omit both to list reviews with optional filtering.",
        parameters=ReadReviewParams,
        handler=read_review,
        actions={"review": {"read": True}},
    ),
    ToolDefinition(
        method="create_review",
        name="Create Review",
        description="Create a new review for a product or channel with optional rating, author, and custom fields.",
        parameters=CreateReviewParams,
        handler=create_review,
        actions={"review": {"create": True}},
    ),
    ToolDefinition(
        method="update_review",
        name="Update Review",
        description="Apply update actions to an existing review identified by id or key.",
        parameters=UpdateReviewParams,
        handler=update_review,
        actions={"review": {"update": True}},
    ),
]

for _tool in _REVIEWS_TOOLS:
    register_tool(_tool)
