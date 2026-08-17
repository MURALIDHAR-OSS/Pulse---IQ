"""Source-independent contracts for normalized consumer reviews."""

from datetime import date, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ReviewDataKind(StrEnum):
    """How review records were obtained and may be presented."""

    DEMO = "demo"
    PERMITTED_LIVE = "permitted_live"


class ReviewProvenance(BaseModel):
    """Source and collection context retained with every normalized review."""

    provider_id: str
    provider_name: str
    data_kind: ReviewDataKind
    retrieved_at: datetime
    source_review_id: str | None = None
    source_url: str | None = None
    attribution: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Review(BaseModel):
    """Canonical review object consumed by future analytical pipelines."""

    review_id: str
    product_id: str
    text: str = Field(min_length=1)
    rating: float | None = Field(default=None, ge=0)
    rating_scale: float | None = Field(default=None, gt=0)
    review_date: date | None = None
    language: str | None = None
    provenance: ReviewProvenance


class ReviewListResponse(BaseModel):
    """Reviews returned for a canonical product from one provider."""

    product_id: str
    provider_id: str
    data_kind: ReviewDataKind
    dataset_label: str
    reviews: list[Review]
