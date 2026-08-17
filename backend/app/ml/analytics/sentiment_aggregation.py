"""Deterministic aggregation of review-level model sentiment results."""

from decimal import Decimal, ROUND_HALF_UP

from app.schemas.sentiment import ReviewSentimentResult
from app.schemas.sentiment_aggregation import AggregateSentimentStatistics


class SentimentAggregationService:
    """Produce count-based consumer sentiment statistics without model re-inference."""

    _SUPPORTED_LABELS = ("positive", "neutral", "negative")
    _ONE_DECIMAL_PLACE = Decimal("0.1")
    _HUNDRED = Decimal("100")

    def aggregate(
        self,
        sentiment_results: list[ReviewSentimentResult] | tuple[ReviewSentimentResult, ...],
        reviews_received: int,
    ) -> AggregateSentimentStatistics:
        """Aggregate already-classified results against the explicitly supplied received count."""
        if reviews_received < 0:
            raise ValueError("reviews_received must be non-negative.")
        if len(sentiment_results) > reviews_received:
            raise ValueError("Analyzed review results cannot exceed reviews_received.")

        counts = {label: 0 for label in self._SUPPORTED_LABELS}
        for result in sentiment_results:
            label = result.sentiment_label.strip().lower()
            if label not in counts:
                raise ValueError(f"Unsupported sentiment label: {result.sentiment_label!r}")
            counts[label] += 1

        total_analyzed = len(sentiment_results)
        positive_percentage = self._percentage(counts["positive"], total_analyzed)
        neutral_percentage = self._percentage(counts["neutral"], total_analyzed)
        negative_percentage = self._percentage(counts["negative"], total_analyzed)
        net_sentiment_score = self._round(positive_percentage - negative_percentage)
        average_confidence = self._average_confidence_percentage(sentiment_results)
        coverage = self._percentage(total_analyzed, reviews_received)

        return AggregateSentimentStatistics(
            reviews_received=reviews_received,
            total_analyzed_reviews=total_analyzed,
            positive_count=counts["positive"],
            neutral_count=counts["neutral"],
            negative_count=counts["negative"],
            positive_percentage=float(positive_percentage),
            neutral_percentage=float(neutral_percentage),
            negative_percentage=float(negative_percentage),
            net_sentiment_score=float(net_sentiment_score),
            average_model_confidence_percentage=float(average_confidence),
            analysis_coverage_percentage=float(coverage),
        )

    def _percentage(self, count: int, total: int) -> Decimal:
        if total == 0:
            return Decimal("0.0")
        return self._round(Decimal(count) / Decimal(total) * self._HUNDRED)

    def _average_confidence_percentage(
        self, sentiment_results: list[ReviewSentimentResult] | tuple[ReviewSentimentResult, ...]
    ) -> Decimal:
        if not sentiment_results:
            return Decimal("0.0")
        total_confidence = sum((Decimal(str(result.model_confidence)) for result in sentiment_results), Decimal("0"))
        return self._round(total_confidence / Decimal(len(sentiment_results)) * self._HUNDRED)

    def _round(self, value: Decimal) -> Decimal:
        return value.quantize(self._ONE_DECIMAL_PLACE, rounding=ROUND_HALF_UP)
