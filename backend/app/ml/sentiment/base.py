"""Stable abstraction for interchangeable review sentiment analyzers."""

from abc import ABC, abstractmethod

from app.schemas.review import Review
from app.schemas.sentiment import ReviewSentimentResult


class SentimentAnalyzer(ABC):
    """Transforms one normalized review into one model sentiment prediction."""

    @abstractmethod
    def analyze(self, review: Review) -> ReviewSentimentResult:
        """Run inference for a review and return a validated sentiment result."""
