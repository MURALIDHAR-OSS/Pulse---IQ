"""Transformer-backed, review-level sentiment analysis."""

from typing import Any

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from app.ml.sentiment.base import SentimentAnalyzer
from app.schemas.review import Review
from app.schemas.sentiment import ReviewSentimentResult


class TransformerSentimentAnalyzer(SentimentAnalyzer):
    """Run real inference with one lazily loaded, reusable Hugging Face model."""

    MODEL_ID = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    def __init__(self, model_id: str = MODEL_ID) -> None:
        self._model_id = model_id
        self._tokenizer: Any | None = None
        self._model: Any | None = None
        self._model_version: str | None = None

    def _ensure_loaded(self) -> None:
        if self._model is not None and self._tokenizer is not None:
            return

        self._tokenizer = AutoTokenizer.from_pretrained(self._model_id)
        self._model = AutoModelForSequenceClassification.from_pretrained(self._model_id)
        self._model.eval()
        self._model_version = (
            getattr(self._model.config, "_commit_hash", None)
            or getattr(self._tokenizer, "_commit_hash", None)
            or "unresolved"
        )

    def analyze(self, review: Review) -> ReviewSentimentResult:
        """Tokenize review text, run model inference, and return softmax confidence."""
        text = review.text.strip()
        if not text:
            raise ValueError("Review text must contain non-whitespace characters.")

        self._ensure_loaded()
        encoded_input = self._tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

        with torch.inference_mode():
            logits = self._model(**encoded_input).logits[0]
            probabilities = torch.softmax(logits, dim=-1)

        predicted_index = int(torch.argmax(probabilities).item())
        model_label = self._model.config.id2label[predicted_index]
        confidence = float(probabilities[predicted_index].item())

        return ReviewSentimentResult(
            review_id=review.review_id,
            sentiment_label=str(model_label).strip().lower(),
            model_confidence=confidence,
            model_identifier=self._model_id,
            model_version=self._model_version or "unresolved",
        )
