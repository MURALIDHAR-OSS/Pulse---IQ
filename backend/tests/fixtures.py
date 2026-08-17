"""Deterministic normalized-review fixtures for ML component tests."""

from app.providers.demo_reviews import DemoReviewProvider
from app.schemas.review import Review


def demo_reviews() -> tuple[Review, ...]:
    """Return existing local demo Review objects without modifying their provenance."""
    return tuple(DemoReviewProvider().list_reviews("apple-iphone-17-pro"))


def review_with_text(review_id: str, text: str) -> Review:
    """Reuse demo-review provenance while supplying a focused test text."""
    return demo_reviews()[0].model_copy(update={"review_id": review_id, "text": text})
