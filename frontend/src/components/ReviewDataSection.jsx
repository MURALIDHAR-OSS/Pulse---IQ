function formatReviewDate(reviewDate) {
  if (!reviewDate) return null
  return new Intl.DateTimeFormat(undefined, { day: 'numeric', month: 'short', year: 'numeric' })
    .format(new Date(`${reviewDate}T00:00:00`))
}

function formatRetrievedAt(retrievedAt) {
  if (!retrievedAt) return null
  return new Intl.DateTimeFormat(undefined, { day: 'numeric', month: 'short', year: 'numeric' })
    .format(new Date(retrievedAt))
}

function ReviewCard({ review }) {
  const { provenance } = review
  const reviewDate = formatReviewDate(review.review_date)
  const retrievedAt = formatRetrievedAt(provenance.retrieved_at)

  return (
    <article className="review-card">
      <div className="review-card-topline">
        <span className="demo-badge">Demo / sample</span>
        {review.rating !== null && review.rating !== undefined && (
          <span className="review-rating">Rating: {review.rating}{review.rating_scale ? ` / ${review.rating_scale}` : ''}</span>
        )}
      </div>
      <p className="review-text">{review.text}</p>
      <dl className="review-provenance">
        <div><dt>Provider</dt><dd>{provenance.provider_name}</dd></div>
        {reviewDate && <div><dt>Review date</dt><dd>{reviewDate}</dd></div>}
        {provenance.source_review_id && <div><dt>Source record</dt><dd>{provenance.source_review_id}</dd></div>}
        {provenance.attribution && <div><dt>Attribution</dt><dd>{provenance.attribution}</dd></div>}
        {retrievedAt && <div><dt>Retrieved</dt><dd>{retrievedAt}</dd></div>}
        {provenance.source_url && (
          <div><dt>Source link</dt><dd><a href={provenance.source_url} target="_blank" rel="noreferrer">View permitted source</a></dd></div>
        )}
      </dl>
    </article>
  )
}

export function ReviewDataSection({ status, data }) {
  return (
    <section className="review-data-section" aria-labelledby="review-data-title" aria-live="polite" aria-busy={status === 'loading'}>
      <div className="review-section-heading">
        <div>
          <p className="eyebrow">Review data</p>
          <h2 id="review-data-title">Available review records</h2>
        </div>
        <span className="demo-badge demo-badge-prominent">Demo / sample data</span>
      </div>

      {status === 'loading' && <p className="review-state">Loading available demo/sample review data…</p>}
      {status === 'error' && <p className="review-state review-state-error">Demo review data could not be loaded. Product information is still available.</p>}
      {status === 'success' && data.reviews.length === 0 && (
        <p className="review-state">No demo/sample reviews are available for this product yet.</p>
      )}
      {status === 'success' && data.reviews.length > 0 && (
        <>
          <p className="demo-dataset-notice">{data.dataset_label}</p>
          <div className="review-list">
            {data.reviews.map((review) => <ReviewCard key={review.review_id} review={review} />)}
          </div>
        </>
      )}
    </section>
  )
}
