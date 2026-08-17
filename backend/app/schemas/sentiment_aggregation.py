"""Validated contract for deterministic consumer-level sentiment statistics."""

from decimal import Decimal, ROUND_HALF_UP

from pydantic import BaseModel, Field, model_validator

from app.schemas.review import ReviewDataKind


_ONE_DECIMAL_PLACE = Decimal("0.1")
_HUNDRED = Decimal("100")


def _rounded_percentage(count: int, total: int) -> Decimal:
    if total == 0:
        return Decimal("0.0")
    return (Decimal(count) / Decimal(total) * _HUNDRED).quantize(_ONE_DECIMAL_PLACE, rounding=ROUND_HALF_UP)


class AggregateSentimentStatistics(BaseModel):
    """Count-derived statistics over a caller-supplied set of sentiment results."""

    provider_id: str | None = None
    data_kind: ReviewDataKind | None = None
    dataset_label: str | None = None
    reviews_received: int = Field(ge=0)
    total_analyzed_reviews: int = Field(ge=0)
    positive_count: int = Field(ge=0)
    neutral_count: int = Field(ge=0)
    negative_count: int = Field(ge=0)
    positive_percentage: float = Field(ge=0, le=100)
    neutral_percentage: float = Field(ge=0, le=100)
    negative_percentage: float = Field(ge=0, le=100)
    net_sentiment_score: float = Field(ge=-100, le=100)
    average_model_confidence_percentage: float = Field(ge=0, le=100)
    analysis_coverage_percentage: float = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_integrity(self) -> "AggregateSentimentStatistics":
        if self.positive_count + self.neutral_count + self.negative_count != self.total_analyzed_reviews:
            raise ValueError("Sentiment counts must equal total_analyzed_reviews.")
        if self.total_analyzed_reviews > self.reviews_received:
            raise ValueError("total_analyzed_reviews cannot exceed reviews_received.")
        expected_percentages = (
            _rounded_percentage(self.positive_count, self.total_analyzed_reviews),
            _rounded_percentage(self.neutral_count, self.total_analyzed_reviews),
            _rounded_percentage(self.negative_count, self.total_analyzed_reviews),
        )
        actual_percentages = (
            Decimal(str(self.positive_percentage)),
            Decimal(str(self.neutral_percentage)),
            Decimal(str(self.negative_percentage)),
        )
        if actual_percentages != expected_percentages:
            raise ValueError("Sentiment percentages must be derived from sentiment counts.")
        expected_net_sentiment = (expected_percentages[0] - expected_percentages[2]).quantize(
            _ONE_DECIMAL_PLACE, rounding=ROUND_HALF_UP
        )
        if Decimal(str(self.net_sentiment_score)) != expected_net_sentiment:
            raise ValueError("net_sentiment_score must equal positive_percentage minus negative_percentage.")
        expected_coverage = _rounded_percentage(self.total_analyzed_reviews, self.reviews_received)
        if Decimal(str(self.analysis_coverage_percentage)) != expected_coverage:
            raise ValueError("analysis_coverage_percentage must be derived from analyzed and received counts.")
        if self.total_analyzed_reviews == 0 and self.average_model_confidence_percentage != 0:
            raise ValueError("Empty aggregations must have zero average_model_confidence_percentage.")
        return self
