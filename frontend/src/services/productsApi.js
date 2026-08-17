export async function searchProducts(query, signal) {
  const response = await fetch(`/api/v1/products/search?q=${encodeURIComponent(query)}`, {
    signal,
  })

  if (!response.ok) {
    throw new Error('Product search is unavailable. Please try again.')
  }

  return response.json()
}

export async function getProduct(productId, signal) {
  const response = await fetch(`/api/v1/products/${encodeURIComponent(productId)}`, { signal })

  if (!response.ok) {
    const error = new Error(response.status === 404 ? 'Product not found.' : 'Product lookup is unavailable.')
    error.status = response.status
    throw error
  }

  return response.json()
}

export async function getProductReviews(productId, signal) {
  const response = await fetch(`/api/v1/products/${encodeURIComponent(productId)}/reviews`, { signal })

  if (!response.ok) {
    const error = new Error('Demo review data is unavailable.')
    error.status = response.status
    throw error
  }

  return response.json()
}
