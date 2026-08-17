from fastapi import APIRouter, HTTPException, Query

from app.catalog.products import get_product_by_id, search_products
from app.schemas.product import Product, ProductSearchResponse

router = APIRouter(tags=["products"])


@router.get("/products/search", response_model=ProductSearchResponse)
def product_search(
    q: str = Query(..., min_length=1, max_length=120, description="Product search query"),
) -> ProductSearchResponse:
    """Search the deterministic local product catalog."""
    products = search_products(q)
    return ProductSearchResponse(query=q.strip(), results=products)


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str) -> Product:
    """Get one canonical product by its stable local catalog identifier."""
    product = get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product
