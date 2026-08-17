export async function searchProducts(query, signal) {
  const response = await fetch(`/api/v1/products/search?q=${encodeURIComponent(query)}`, {
    signal,
  })

  if (!response.ok) {
    throw new Error('Product search is unavailable. Please try again.')
  }

  return response.json()
}
