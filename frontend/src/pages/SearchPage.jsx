import { useState } from 'react'
import { Link } from 'react-router-dom'
import { searchProducts } from '../services/productsApi'

export function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [searchedQuery, setSearchedQuery] = useState('')
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    const trimmedQuery = query.trim()
    if (!trimmedQuery) return

    setStatus('loading')
    setError('')
    setResults([])
    setSearchedQuery(trimmedQuery)

    try {
      const data = await searchProducts(trimmedQuery)
      setResults(data.results)
      setStatus('success')
    } catch (requestError) {
      setError(requestError.message)
      setStatus('error')
    }
  }

  return (
    <>
      <section className="search-hero" aria-labelledby="page-title">
        <p className="eyebrow">Consumer intelligence, starting with the product</p>
        <h1 id="page-title">Find the product you want to understand.</h1>
        <p className="hero-copy">Search our local product catalog to begin a future PulseIQ analysis.</p>

        <form className="search-form" onSubmit={handleSubmit}>
          <label className="sr-only" htmlFor="product-search">Search products</label>
          <input
            id="product-search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder={'Try "iPhone 17 Pro"'}
            autoComplete="off"
          />
          <button type="submit" disabled={!query.trim() || status === 'loading'}>
            {status === 'loading' ? 'Searching…' : 'Search'}
          </button>
        </form>
      </section>

      <section className="results-section" aria-live="polite" aria-busy={status === 'loading'}>
        {status === 'idle' && <p className="results-hint">Search for a product to see matching canonical products.</p>}
        {status === 'loading' && <p className="results-hint">Searching the local catalog…</p>}
        {status === 'error' && <p className="message error-message">{error}</p>}
        {status === 'success' && results.length === 0 && (
          <p className="message">No products matched “{searchedQuery}” in the local catalog.</p>
        )}
        {status === 'success' && results.length > 0 && (
          <>
            <div className="results-heading">
              <h2>Matching products</h2>
              <p>{results.length} result{results.length === 1 ? '' : 's'} for “{searchedQuery}”</p>
            </div>
            <ul className="product-grid">
              {results.map((product) => (
                <li key={product.id}>
                  <Link className="product-card" to={`/products/${encodeURIComponent(product.id)}`}>
                    <div className="product-monogram" aria-hidden="true">{product.brand.slice(0, 1)}</div>
                    <div>
                      <p className="product-category">{product.category}</p>
                      <h3>{product.name}</h3>
                      <p className="product-brand">{product.brand}</p>
                    </div>
                    <span className="card-arrow" aria-hidden="true">→</span>
                  </Link>
                </li>
              ))}
            </ul>
          </>
        )}
      </section>
    </>
  )
}
