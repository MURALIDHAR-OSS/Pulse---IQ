# Enhanced Sentiment Aggregation

## Inputs and scope

The aggregation service accepts only existing `ReviewSentimentResult` objects
and an explicit `reviews_received` count supplied by the caller. It does not
load a model, inspect review text, call an LLM, or invent missing review counts.

## Sentiment distribution

For each supported label, PulseIQ counts the actual included results:

```text
sentiment percentage = (sentiment count / total analyzed reviews) × 100
```

The total analyzed count is the number of included valid result objects, and
the positive, neutral, and negative counts must sum to that total. Model
confidence is never used to calculate these percentages.

## Rounding

All displayed percentages and derived decimal statistics use `Decimal` and
`ROUND_HALF_UP` to one decimal place. Categories are rounded independently, so
thirds can display as `33.3`, `33.3`, and `33.3`; this is display rounding, not
a count inconsistency. Empty input produces zero counts and `0.0` for every
derived metric without dividing by zero.

## Net Sentiment Score

```text
net sentiment score = positive percentage - negative percentage
```

The result is constrained to the range `-100.0` through `100.0`. It is derived
from the already count-derived displayed percentages and never from confidence.

## Average model confidence

```text
average model confidence percentage = mean(model_confidence) × 100
```

The output uses a `0.0`–`100.0` scale and one decimal place for dashboard
readability. It remains a separate descriptive statistic: it is not sentiment
percentage, consumer reliability, model accuracy, or an arbitrary AI score.

## Analysis coverage

```text
analysis coverage percentage = (total analyzed reviews / reviews received) × 100
```

`reviews_received` must be explicitly supplied. The service never assumes it
equals the analyzed count. Analyzed reviews cannot exceed received reviews;
when both are zero, coverage is `0.0`.

## Integrity and limitations

The schema enforces non-negative counts, count-total consistency, percentage
bounds, confidence bounds, net-sentiment bounds, and coverage bounds. Unknown
sentiment labels are rejected. This deterministic layer makes no model-accuracy
claim and does not perform LLM numerical aggregation.
