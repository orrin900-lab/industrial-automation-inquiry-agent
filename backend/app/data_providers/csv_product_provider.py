from pathlib import Path

from app.data_access.product_repository import (
    ProductRepository,
    normalize_category,
    product_to_search_text,
)
from app.data_providers.product_provider import ProductDataProvider
from app.schemas.product import Product


class CSVProductProvider(ProductDataProvider):
    provider_name = "csv"

    def __init__(
        self,
        csv_path: Path | None = None,
        *,
        fallback_reason: str | None = None,
    ) -> None:
        self.repository = ProductRepository(csv_path=csv_path)
        self.fallback_reason = fallback_reason

    def list_products(self, product_category: str | None = None) -> list[Product]:
        return self.repository.list_products(product_category)

    def get_product_by_id(self, product_id: str) -> Product | None:
        normalized_id = product_id.strip().lower()
        for product in self.repository.list_products():
            if product.product_id.lower() == normalized_id:
                return product
        return None

    def search_products(
        self,
        query: str,
        product_category: str | None = None,
        limit: int | None = None,
    ) -> list[Product]:
        normalized_category = normalize_category(product_category)
        query_tokens = [
            token
            for token in query.lower().replace("/", " ").replace("-", " ").split()
            if len(token) > 1
        ]
        products = self.repository.list_products(normalized_category)
        if not query_tokens:
            return products[:limit] if limit else products

        scored: list[tuple[int, Product]] = []
        for product in products:
            product_text = product_to_search_text(product)
            score = sum(1 for token in query_tokens if token in product_text)
            if score > 0:
                scored.append((score, product))

        scored.sort(key=lambda item: item[0], reverse=True)
        results = [product for _, product in scored]
        return results[:limit] if limit else results

