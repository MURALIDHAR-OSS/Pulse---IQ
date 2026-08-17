"""Small synthetic sample dataset for local PulseIQ development only."""

from datetime import UTC, date, datetime

from app.providers.base import ReviewProvider
from app.schemas.review import Review, ReviewDataKind, ReviewProvenance


class DemoReviewProvider(ReviewProvider):
    """Provides curated sample reviews; no records originate from external platforms."""

    provider_id = "pulseiq-demo"
    provider_name = "PulseIQ Demo Review Provider"
    data_kind = ReviewDataKind.DEMO
    dataset_label = "Demo/sample data created for PulseIQ development; not real platform reviews."

    def __init__(self) -> None:
        retrieved_at = datetime(2026, 8, 17, 0, 0, tzinfo=UTC)
        self._reviews: tuple[Review, ...] = (
            Review(
                review_id="demo-iphone-17-pro-001",
                product_id="apple-iphone-17-pro",
                text="Sample development review: setup was straightforward and daily navigation felt responsive.",
                rating=4.0,
                rating_scale=5.0,
                review_date=date(2026, 7, 10),
                language="en",
                provenance=self._provenance(retrieved_at, "demo-review-001"),
            ),
            Review(
                review_id="demo-iphone-17-pro-002",
                product_id="apple-iphone-17-pro",
                text="Sample development review: the display was comfortable for reading during a commute.",
                rating=5.0,
                rating_scale=5.0,
                review_date=date(2026, 7, 18),
                language="en",
                provenance=self._provenance(retrieved_at, "demo-review-002"),
            ),
            Review(
                review_id="demo-galaxy-s26-ultra-001",
                product_id="samsung-galaxy-s26-ultra",
                text="Sample development review: the large screen was useful for maps and video calls.",
                rating=None,
                rating_scale=None,
                review_date=None,
                language="en",
                provenance=self._provenance(retrieved_at, "demo-review-003"),
            ),
        )

    def _provenance(self, retrieved_at: datetime, source_review_id: str) -> ReviewProvenance:
        return ReviewProvenance(
            provider_id=self.provider_id,
            provider_name=self.provider_name,
            data_kind=self.data_kind,
            retrieved_at=retrieved_at,
            source_review_id=source_review_id,
            attribution="PulseIQ synthetic demo/sample review for local development.",
            metadata={"synthetic": True, "usage": "development_and_testing"},
        )

    def list_reviews(self, product_id: str) -> list[Review]:
        return [review for review in self._reviews if review.product_id == product_id]
