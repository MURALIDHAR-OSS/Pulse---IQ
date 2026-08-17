from fastapi import APIRouter, Query

from app.catalog.products import search_products
from app.schemas.product import ProductSearchResponse

router = APIRouter(tags=["products"])


@router.get("/products/search", response_model=ProductSearchResponse)
def product_search(
    q: str = Query(..., min_length=1, max_length=120, description="Product search query"),
) -> ProductSearchResponse:
    """Search the deterministic local product catalog."""
    products = search_products(q)
    return ProductSearchResponse(query=q.strip(), results=products)
