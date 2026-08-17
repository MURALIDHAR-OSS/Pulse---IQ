"""Demo review-data API routes."""

from fastapi import APIRouter, HTTPException

from app.catalog.products import get_product_by_id
from app.providers.demo_reviews import DemoReviewProvider
from app.schemas.review import ReviewListResponse
from app.services.reviews import ReviewService

router = APIRouter(tags=["reviews"])
review_service = ReviewService(DemoReviewProvider())


@router.get("/products/{product_id}/reviews", response_model=ReviewListResponse)
def list_product_reviews(product_id: str) -> ReviewListResponse:
    """Return clearly labelled demo/sample reviews for a canonical product."""
    if get_product_by_id(product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    return review_service.get_reviews_for_product(product_id)
