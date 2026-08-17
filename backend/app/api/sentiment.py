"""Sentiment-intelligence API routes backed by real analysis and aggregation."""

import logging

from fastapi import APIRouter, HTTPException

from app.catalog.products import get_product_by_id
from app.ml.analytics.sentiment_aggregation import SentimentAggregationService
from app.ml.sentiment.transformer import TransformerSentimentAnalyzer
from app.providers.demo_reviews import DemoReviewProvider
from app.schemas.sentiment_aggregation import AggregateSentimentStatistics
from app.services.reviews import ReviewService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["sentiment"])
review_service = ReviewService(DemoReviewProvider())
sentiment_analyzer = TransformerSentimentAnalyzer()
aggregation_service = SentimentAggregationService()


@router.get("/products/{product_id}/sentiment", response_model=AggregateSentimentStatistics)
def get_product_sentiment(product_id: str) -> AggregateSentimentStatistics:
    """Analyze local demo reviews and return deterministic consumer sentiment statistics."""
    if get_product_by_id(product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    review_response = review_service.get_reviews_for_product(product_id)
    try:
        sentiment_results = [sentiment_analyzer.analyze(review) for review in review_response.reviews]
        statistics = aggregation_service.aggregate(
            sentiment_results=sentiment_results,
            reviews_received=len(review_response.reviews),
        )
    except Exception as error:
        logger.exception("Sentiment analysis failed for product_id=%s", product_id)
        raise HTTPException(status_code=500, detail="Sentiment analysis is unavailable.") from error

    return statistics.model_copy(
        update={
            "provider_id": review_response.provider_id,
            "data_kind": review_response.data_kind,
            "dataset_label": review_response.dataset_label,
        }
    )
