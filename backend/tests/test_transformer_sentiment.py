"""Integration tests for real Transformer sentiment inference."""

import math
import unittest

from app.ml.sentiment.transformer import TransformerSentimentAnalyzer
from app.schemas.sentiment import ReviewSentimentResult
from tests.fixtures import demo_reviews, review_with_text


class TransformerSentimentAnalyzerTests(unittest.TestCase):
    """Exercise actual model inference; these tests do not mock model outputs."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.analyzer = TransformerSentimentAnalyzer()

    def test_clearly_positive_review(self) -> None:
        result = self.analyzer.analyze(
            review_with_text("test-positive-review", "This product is excellent. I love it and would buy it again.")
        )
        self.assertEqual(result.sentiment_label, "positive")

    def test_clearly_negative_review(self) -> None:
        result = self.analyzer.analyze(
            review_with_text("test-negative-review", "This product is terrible. I hate it and regret buying it.")
        )
        self.assertEqual(result.sentiment_label, "negative")

    def test_blank_review_text_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.analyzer.analyze(review_with_text("test-blank-review", "   "))

    def test_output_is_valid_schema_with_model_probability(self) -> None:
        result = self.analyzer.analyze(demo_reviews()[0])
        self.assertIsInstance(result, ReviewSentimentResult)
        self.assertEqual(result.review_id, "demo-iphone-17-pro-001")
        self.assertTrue(math.isfinite(result.model_confidence))
        self.assertGreaterEqual(result.model_confidence, 0)
        self.assertLessEqual(result.model_confidence, 1)
        self.assertTrue(result.model_identifier.startswith("cardiffnlp/"))
        self.assertTrue(result.model_version)

    def test_loaded_model_is_reused_for_multiple_reviews(self) -> None:
        self.analyzer.analyze(demo_reviews()[0])
        first_model_instance = self.analyzer._model
        self.analyzer.analyze(demo_reviews()[1])
        self.assertIs(self.analyzer._model, first_model_instance)


if __name__ == "__main__":
    unittest.main()
