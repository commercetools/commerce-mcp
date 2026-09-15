from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class ReadStateParams(BaseModel):
    id: str | None = None
    key: str | None = None
    where: list[str] | None = None
    limit: int | None = Field(None, ge=1, le=500)
    offset: int | None = Field(None, ge=0)
    sort: list[str] | None = None
    expand: list[str] | None = None

    model_config = {"populate_by_name": True}


StateType = Literal[
    "OrderState",
    "RecurringOrderState",
    "LineItemState",
    "ProductState",
    "ReviewState",
    "PaymentState",
    "QuoteRequestState",
    "StagedQuoteState",
    "QuoteState",
]

StateRole = Literal["ReviewIncludedInStatistics", "Return"]


class StateTransitionRef(BaseModel):
    id: str
    type_id: Literal["state"] = Field("state", alias="typeId")

    model_config = {"populate_by_name": True}


class CreateStateParams(BaseModel):
    key: str
    type: StateType
    initial: bool | None = None
    name: dict[str, str] | None = None
    description: dict[str, str] | None = None
    roles: list[StateRole] | None = None
    transitions: list[dict] | None = None

    model_config = {"populate_by_name": True}


class UpdateStateParams(BaseModel):
    id: str | None = None
    key: str | None = None
    version: int
    actions: list[dict]

    model_config = {"populate_by_name": True}
