"""Provider-neutral review retrieval service."""

from app.providers.base import ReviewProvider
from app.schemas.review import ReviewListResponse


class ReviewService:
    """Expose normalized reviews without coupling callers to a provider implementation."""

    def __init__(self, provider: ReviewProvider) -> None:
        self._provider = provider

    def get_reviews_for_product(self, product_id: str) -> ReviewListResponse:
        return ReviewListResponse(
            product_id=product_id,
            provider_id=self._provider.provider_id,
            data_kind=self._provider.data_kind,
            dataset_label=self._provider.dataset_label,
            reviews=self._provider.list_reviews(product_id),
        )
