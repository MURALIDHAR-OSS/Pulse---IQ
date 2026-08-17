"""Focused API orchestration tests for the sentiment-intelligence endpoint."""

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import sentiment as sentiment_api
from app.schemas.sentiment import ReviewSentimentResult
from app.schemas.sentiment_aggregation import AggregateSentimentStatistics
from main import app


class SentimentApiTests(unittest.TestCase):
    """Verify routing and composition without replacing production ML behavior."""

    def setUp(self) -> None:
        self.client = TestClient(app)

    @staticmethod
    def _prediction_for(review_id: str) -> ReviewSentimentResult:
        return ReviewSentimentResult(
            review_id=review_id,
            sentiment_label="positive",
            model_confidence=0.91,
            model_identifier="test-model",
            model_version="test-version",
        )

    def test_valid_product_with_demo_reviews(self) -> None:
        with patch.object(
            sentiment_api.sentiment_analyzer,
            "analyze",
            side_effect=lambda review: self._prediction_for(review.review_id),
        ) as analyze:
            response = self.client.get("/api/v1/products/apple-iphone-17-pro/sentiment")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["data_kind"], "demo")
        self.assertIn("Demo/sample", body["dataset_label"])
        self.assertEqual(body["provider_id"], "pulseiq-demo")
        self.assertEqual(body["total_analyzed_reviews"], 2)
        self.assertEqual(body["positive_count"], 2)
        self.assertEqual(body["positive_percentage"], 100.0)
        self.assertEqual(body["analysis_coverage_percentage"], 100.0)
        self.assertEqual(analyze.call_count, 2)

    def test_valid_product_without_demo_reviews_returns_empty_analysis(self) -> None:
        with patch.object(sentiment_api.sentiment_analyzer, "analyze") as analyze:
            response = self.client.get("/api/v1/products/apple-iphone-17/sentiment")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["data_kind"], "demo")
        self.assertEqual(body["total_analyzed_reviews"], 0)
        self.assertEqual(body["positive_count"], 0)
        self.assertEqual(body["neutral_count"], 0)
        self.assertEqual(body["negative_count"], 0)
        self.assertEqual(body["analysis_coverage_percentage"], 0.0)
        analyze.assert_not_called()

    def test_unknown_product_returns_not_found(self) -> None:
        with patch.object(sentiment_api.sentiment_analyzer, "analyze") as analyze:
            response = self.client.get("/api/v1/products/unknown-product/sentiment")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Product not found.")
        analyze.assert_not_called()

    def test_response_is_valid_aggregate_schema(self) -> None:
        with patch.object(
            sentiment_api.sentiment_analyzer,
            "analyze",
            side_effect=lambda review: self._prediction_for(review.review_id),
        ):
            response = self.client.get("/api/v1/products/apple-iphone-17-pro/sentiment")

        validated = AggregateSentimentStatistics.model_validate(response.json())
        self.assertEqual(validated.total_analyzed_reviews, 2)


if __name__ == "__main__":
    unittest.main()
