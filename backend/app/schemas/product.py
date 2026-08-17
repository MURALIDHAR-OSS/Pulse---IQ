from pydantic import BaseModel, Field


class Product(BaseModel):
    """Canonical product identity exposed by the local catalog."""

    id: str = Field(description="Stable canonical product identifier")
    name: str
    brand: str
    category: str
    image_url: str | None = None
    aliases: list[str] = Field(default_factory=list)


class ProductSearchResponse(BaseModel):
    query: str
    results: list[Product]
