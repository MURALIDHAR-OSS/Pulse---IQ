"""Deterministic tests for count-based aggregate sentiment statistics."""

import unittest

from pydantic import ValidationError

from app.ml.analytics.sentiment_aggregation import SentimentAggregationService
from app.schemas.sentiment_aggregation import AggregateSentimentStatistics
from tests.fixtures import sentiment_result, sentiment_results


class SentimentAggregationServiceTests(unittest.TestCase):
    """Verify aggregate metrics are mathematically derived from classified results."""

    def setUp(self) -> None:
        self.service = SentimentAggregationService()

    def test_known_distribution(self) -> None:
        result = self.service.aggregate(sentiment_results(positive_count=7, neutral_count=2, negative_count=1), 10)
        self.assertEqual(result.total_analyzed_reviews, 10)
        self.assertEqual((result.positive_count, result.neutral_count, result.negative_count), (7, 2, 1))
        self.assertEqual((result.positive_percentage, result.neutral_percentage, result.negative_percentage), (70.0, 20.0, 10.0))
        self.assertEqual(result.net_sentiment_score, 60.0)

    def test_all_single_label_distributions(self) -> None:
        for positive, neutral, negative, expected in ((3, 0, 0, "positive"), (0, 3, 0, "neutral"), (0, 0, 3, "negative")):
            with self.subTest(expected=expected):
                result = self.service.aggregate(sentiment_results(positive, neutral, negative), 3)
                self.assertEqual(getattr(result, f"{expected}_percentage"), 100.0)
                self.assertEqual(result.total_analyzed_reviews, 3)

    def test_empty_input_is_safe(self) -> None:
        result = self.service.aggregate([], 0)
        self.assertEqual(result.total_analyzed_reviews, 0)
        self.assertEqual((result.positive_count, result.neutral_count, result.negative_count), (0, 0, 0))
        self.assertEqual((result.positive_percentage, result.neutral_percentage, result.negative_percentage), (0.0, 0.0, 0.0))
        self.assertEqual((result.net_sentiment_score, result.average_model_confidence_percentage, result.analysis_coverage_percentage), (0.0, 0.0, 0.0))

    def test_one_third_rounding_uses_half_up_to_one_decimal(self) -> None:
        result = self.service.aggregate(sentiment_results(positive_count=1, negative_count=2), 3)
        self.assertEqual(result.positive_percentage, 33.3)
        self.assertEqual(result.negative_percentage, 66.7)

    def test_average_model_confidence_is_separate_from_distribution(self) -> None:
        results = [
            sentiment_result("one", "positive", 0.90),
            sentiment_result("two", "neutral", 0.80),
            sentiment_result("three", "negative", 0.95),
        ]
        result = self.service.aggregate(results, 3)
        self.assertEqual(result.average_model_confidence_percentage, 88.3)
        self.assertEqual((result.positive_percentage, result.neutral_percentage, result.negative_percentage), (33.3, 33.3, 33.3))

    def test_same_labels_with_different_confidences_keep_same_percentages(self) -> None:
        low_confidence = [
            sentiment_result("low-1", "positive", 0.01),
            sentiment_result("low-2", "positive", 0.02),
            sentiment_result("low-3", "negative", 0.03),
        ]
        high_confidence = [
            sentiment_result("high-1", "positive", 0.99),
            sentiment_result("high-2", "positive", 0.98),
            sentiment_result("high-3", "negative", 0.97),
        ]
        low_result = self.service.aggregate(low_confidence, 3)
        high_result = self.service.aggregate(high_confidence, 3)
        self.assertEqual(
            (low_result.positive_percentage, low_result.neutral_percentage, low_result.negative_percentage),
            (high_result.positive_percentage, high_result.neutral_percentage, high_result.negative_percentage),
        )
        self.assertNotEqual(low_result.average_model_confidence_percentage, high_result.average_model_confidence_percentage)

    def test_coverage_uses_explicit_received_count(self) -> None:
        result = self.service.aggregate(sentiment_results(positive_count=80), 100)
        self.assertEqual(result.analysis_coverage_percentage, 80.0)

    def test_zero_received_with_reviews_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.service.aggregate(sentiment_results(positive_count=1), 0)

    def test_analyzed_greater_than_received_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.service.aggregate(sentiment_results(positive_count=2), 1)

    def test_unsupported_label_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.service.aggregate([sentiment_result("unsupported", "mixed", 0.5)], 1)

    def test_schema_rejects_count_inconsistency_and_bounds_violations(self) -> None:
        valid_values = {
            "reviews_received": 10,
            "total_analyzed_reviews": 10,
            "positive_count": 7,
            "neutral_count": 2,
            "negative_count": 1,
            "positive_percentage": 70.0,
            "neutral_percentage": 20.0,
            "negative_percentage": 10.0,
            "net_sentiment_score": 60.0,
            "average_model_confidence_percentage": 80.0,
            "analysis_coverage_percentage": 100.0,
        }
        with self.assertRaises(ValidationError):
            AggregateSentimentStatistics(**(valid_values | {"negative_count": 2}))
        with self.assertRaises(ValidationError):
            AggregateSentimentStatistics(**(valid_values | {"positive_percentage": 100.1}))
        with self.assertRaises(ValidationError):
            AggregateSentimentStatistics(**(valid_values | {"average_model_confidence_percentage": 100.1}))
        with self.assertRaises(ValidationError):
            AggregateSentimentStatistics(**(valid_values | {"analysis_coverage_percentage": 100.1}))


if __name__ == "__main__":
    unittest.main()
