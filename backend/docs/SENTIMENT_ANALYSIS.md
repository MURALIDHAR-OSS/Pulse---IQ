# Sentiment Analysis Foundation

## Selected model

PulseIQ uses `cardiffnlp/twitter-roberta-base-sentiment-latest`, a pretrained
RoBERTa sequence-classification model published by Cardiff NLP on Hugging Face.
The model card is the implementation source and usage reference:
https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest

The model provides Negative, Neutral, and Positive labels. The analyzer reads
the predicted label from the loaded model configuration rather than maintaining
an independent label mapping.

## Prototype rationale

This is a practical first prototype because it is a ready-to-run, English,
three-class sentiment model compatible with the existing PyTorch and
Transformers environment. It gives PulseIQ a real, replaceable inference layer
without training a model from scratch.

## Confidence

For each normalized `Review`, PulseIQ tokenizes the real review text and runs
the loaded model in inference mode. It applies softmax to the model logits and
uses the probability of the model's selected class as `model_confidence`.
This is a per-review model probability, not an aggregate consumer sentiment
percentage and not a count-derived metric.

## Limitations

The selected model was trained on tweets and fine-tuned with TweetEval, rather
than on a labelled consumer-product-review dataset. Product-review language,
domains, and rating conventions may differ. Model confidence is not a guarantee
of correctness or calibration for PulseIQ's target domain. No evaluation has
yet been run on a proper labelled consumer-review dataset, so PulseIQ makes no
accuracy claim for this model.

This foundation performs only review-level sentiment inference. It does not
perform aspect sentiment, complaint detection, topics, embeddings, trends, or
aggregate sentiment percentages.
