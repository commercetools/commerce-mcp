from __future__ import annotations

from pydantic import BaseModel, Field


class ReadProductSelectionProductParams(BaseModel):
    product_selection_id: str | None = Field(None, alias="productSelectionId")
    product_selection_key: str | None = Field(None, alias="productSelectionKey")
    where: list[str] | None = None
    limit: int | None = Field(None, ge=1, le=500)
    offset: int | None = Field(None, ge=0)
    sort: list[str] | None = None
    expand: list[str] | None = None

    model_config = {"populate_by_name": True}
