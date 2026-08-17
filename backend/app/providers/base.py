"""Provider contract for returning normalized review records."""

from abc import ABC, abstractmethod

from app.schemas.review import Review, ReviewDataKind


class ReviewProvider(ABC):
    """Source-independent interface implemented by permitted review providers."""

    provider_id: str
    provider_name: str
    data_kind: ReviewDataKind
    dataset_label: str

    @abstractmethod
    def list_reviews(self, product_id: str) -> list[Review]:
        """Return normalized reviews for one canonical product identifier."""
