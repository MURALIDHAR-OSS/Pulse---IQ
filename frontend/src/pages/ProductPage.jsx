import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { IntelligencePlaceholder } from '../components/IntelligencePlaceholder'
import { ReviewDataSection } from '../components/ReviewDataSection'
import { StatePanel } from '../components/StatePanel'
import { getProduct, getProductReviews } from '../services/productsApi'

const PLACEHOLDER_SECTIONS = [
  ['Consumer verdict', 'A grounded consumer verdict will appear here when permitted review intelligence is available.'],
  ['Strengths and weaknesses', 'Product strengths and weaknesses will be derived from future review analysis.'],
  ['Aspect-level insights', 'Aspect sentiment and mention patterns will be available after analysis is implemented.'],
  ['Complaints', 'Complaint themes and counts are not available until review data is analyzed.'],
  ['Source intelligence', 'Source-wise review intelligence will appear only for permitted data sources.'],
  ['Trends and evidence', 'Time-based signals and supporting evidence will be shown when available.'],
]

export function ProductPage() {
  const { productId } = useParams()
  const [product, setProduct] = useState(null)
  const [status, setStatus] = useState('loading')
  const [reviewData, setReviewData] = useState(null)
  const [reviewStatus, setReviewStatus] = useState('idle')

  useEffect(() => {
    const controller = new AbortController()

    async function loadProduct() {
      setStatus('loading')
      setProduct(null)
      setReviewData(null)
      setReviewStatus('idle')
      try {
        const data = await getProduct(productId, controller.signal)
        setProduct(data)
        setStatus('success')
      } catch (requestError) {
        if (requestError.name !== 'AbortError') {
          setStatus(requestError.status === 404 ? 'not-found' : 'error')
        }
      }
    }

    loadProduct()
    return () => controller.abort()
  }, [productId])

  useEffect(() => {
    if (!product) return undefined

    const controller = new AbortController()

    async function loadReviews() {
      setReviewStatus('loading')
      try {
        const data = await getProductReviews(product.id, controller.signal)
        setReviewData(data)
        setReviewStatus('success')
      } catch (requestError) {
        if (requestError.name !== 'AbortError') {
          setReviewStatus('error')
        }
      }
    }

    loadReviews()
    return () => controller.abort()
  }, [product])

  if (status === 'loading') {
    return <StatePanel title="Loading product" description="Retrieving the canonical product from the local catalog." />
  }

  if (status === 'not-found') {
    return <StatePanel title="Product not found" description="This product is not available in the local catalog." actionLabel="Return to search" />
  }

  if (status === 'error') {
    return <StatePanel title="Unable to load product" description="The local product catalog could not be reached. Please try again." actionLabel="Return to search" />
  }

  return (
    <>
      <section className="product-hero" aria-labelledby="product-title">
        <Link className="back-link" to="/">← Search products</Link>
        <div className="product-identity">
          <div className="product-monogram product-monogram-large" aria-hidden="true">{product.brand.slice(0, 1)}</div>
          <div>
            <p className="eyebrow">{product.category}</p>
            <h1 id="product-title">{product.name}</h1>
            <p className="product-hero-brand">{product.brand}</p>
          </div>
        </div>
        <p className="product-page-intro">This is the foundation for PulseIQ Product Intelligence. No consumer-review analysis is available for this product yet.</p>
      </section>

      <section className="intelligence-intro" aria-labelledby="intelligence-title">
        <p className="eyebrow">Product Intelligence</p>
        <h2 id="intelligence-title">Future consumer insights, clearly separated from product identity.</h2>
      </section>

      <ReviewDataSection status={reviewStatus} data={reviewData} />

      <div className="placeholder-grid">
        {PLACEHOLDER_SECTIONS.map(([title, description]) => (
          <IntelligencePlaceholder key={title} title={title} description={description} />
        ))}
      </div>
    </>
  )
}
