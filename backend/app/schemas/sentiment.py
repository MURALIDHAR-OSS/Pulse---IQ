"""Validated contracts for review-level model sentiment predictions."""

from pydantic import BaseModel, Field


class ReviewSentimentResult(BaseModel):
    """A single model prediction for one normalized review."""

    review_id: str
    sentiment_label: str = Field(min_length=1)
    model_confidence: float = Field(ge=0, le=1)
    model_identifier: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
