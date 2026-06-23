from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SortItem(BaseModel):
    field: str = Field(description="The field to sort by")
    order: str = Field(description="The sort order: 'asc' or 'desc'")
    mode: str | None = Field(None, description="Sorting mode for multi-valued fields: 'min' or 'max'")
    field_type: str | None = Field(None, alias="fieldType", description="Data type of the field for non-standard fields")
    model_config = {"populate_by_name": True}


class SearchProductsParams(BaseModel):
    query: dict[str, Any] = Field(description="Search query against searchable Product fields in the search query language")
    sort: list[SortItem] | None = Field(None, description="Controls how results are sorted. Defaults to relevance score descending.")
    limit: int | None = Field(None, ge=0, le=100, description="Maximum number of results per page (0–100, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of results to skip for pagination (0–10000)")
    mark_matching_variants: bool | None = Field(None, alias="markMatchingVariants", description="If true, returns info about which Product Variants match the query")
    product_projection_parameters: dict[str, Any] | None = Field(None, alias="productProjectionParameters", description="Controls data integration with Product Projection parameters")
    facets: list[dict[str, Any]] | None = Field(None, description="Facets to calculate counts, distinct values, or ranges")
    model_config = {"populate_by_name": True}
