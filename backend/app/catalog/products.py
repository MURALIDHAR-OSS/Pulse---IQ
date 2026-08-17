import re

from app.schemas.product import Product


PRODUCT_CATALOG: tuple[Product, ...] = (
    Product(
        id="apple-iphone-17-pro",
        name="iPhone 17 Pro",
        brand="Apple",
        category="Smartphone",
        image_url=None,
        aliases=["iphone 17 pro", "apple iphone 17 pro"],
    ),
    Product(
        id="apple-iphone-17",
        name="iPhone 17",
        brand="Apple",
        category="Smartphone",
        image_url=None,
        aliases=["iphone 17", "apple iphone 17"],
    ),
    Product(
        id="samsung-galaxy-s26-ultra",
        name="Galaxy S26 Ultra",
        brand="Samsung",
        category="Smartphone",
        image_url=None,
        aliases=["galaxy s26 ultra", "samsung s26 ultra"],
    ),
    Product(
        id="google-pixel-11-pro",
        name="Pixel 11 Pro",
        brand="Google",
        category="Smartphone",
        image_url=None,
        aliases=["pixel 11 pro", "google pixel 11 pro"],
    ),
    Product(
        id="sony-wh-1000xm6",
        name="WH-1000XM6",
        brand="Sony",
        category="Headphones",
        image_url=None,
        aliases=["sony wh-1000xm6", "wh1000xm6"],
    ),
)


def get_product_by_id(product_id: str) -> Product | None:
    """Return one canonical product from the local seed catalog."""
    return next((product for product in PRODUCT_CATALOG if product.id == product_id), None)


def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def search_products(query: str) -> list[Product]:
    """Return stable, relevance-ranked matches from the local seed catalog."""
    normalized_query = " ".join(query.lower().split())
    query_tokens = _tokens(normalized_query)
    if not query_tokens:
        return []

    matches: list[tuple[int, Product]] = []
    for product in PRODUCT_CATALOG:
        searchable_values = [product.name, product.brand, product.category, *product.aliases]
        searchable_text = " ".join(searchable_values).lower()
        overlap = len(query_tokens & _tokens(searchable_text))
        if overlap == 0:
            continue

        exact_name_bonus = 100 if normalized_query == product.name.lower() else 0
        substring_bonus = 20 if normalized_query in searchable_text else 0
        matches.append((exact_name_bonus + substring_bonus + overlap, product))

    return [product for _, product in sorted(matches, key=lambda item: (-item[0], item[1].name))]
