"""Deterministic normalized-review fixtures for ML component tests."""

from app.providers.demo_reviews import DemoReviewProvider
from app.schemas.review import Review
from app.schemas.sentiment import ReviewSentimentResult


def demo_reviews() -> tuple[Review, ...]:
    """Return existing local demo Review objects without modifying their provenance."""
    return tuple(DemoReviewProvider().list_reviews("apple-iphone-17-pro"))


def review_with_text(review_id: str, text: str) -> Review:
    """Reuse demo-review provenance while supplying a focused test text."""
    return demo_reviews()[0].model_copy(update={"review_id": review_id, "text": text})


def sentiment_results(
    positive_count: int = 0,
    neutral_count: int = 0,
    negative_count: int = 0,
    confidence: float = 0.75,
) -> list[ReviewSentimentResult]:
    """Build deterministic validated sentiment-result fixtures for aggregation tests."""
    results: list[ReviewSentimentResult] = []
    for label, count in (("positive", positive_count), ("neutral", neutral_count), ("negative", negative_count)):
        results.extend(
            ReviewSentimentResult(
                review_id=f"fixture-{label}-{index}",
                sentiment_label=label,
                model_confidence=confidence,
                model_identifier="fixture-model",
                model_version="fixture-version",
            )
            for index in range(count)
        )
    return results


def sentiment_result(review_id: str, label: str, confidence: float) -> ReviewSentimentResult:
    """Build one deterministic validated sentiment result for a focused test."""
    return ReviewSentimentResult(
        review_id=review_id,
        sentiment_label=label,
        model_confidence=confidence,
        model_identifier="fixture-model",
        model_version="fixture-version",
    )
