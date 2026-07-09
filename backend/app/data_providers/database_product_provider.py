from app.data_providers.product_provider import ProductDataProvider
from app.schemas.product import Product


class DatabaseProductProvider(ProductDataProvider):
    provider_name = "database"

    def list_products(self, product_category: str | None = None) -> list[Product]:
        raise NotImplementedError(
            "DatabaseProductProvider is reserved for a future PostgreSQL product table."
        )

    def get_product_by_id(self, product_id: str) -> Product | None:
        raise NotImplementedError(
            "DatabaseProductProvider is reserved for a future PostgreSQL product table."
        )

    def search_products(
        self,
        query: str,
        product_category: str | None = None,
        limit: int | None = None,
    ) -> list[Product]:
        raise NotImplementedError(
            "DatabaseProductProvider is reserved for a future PostgreSQL product table."
        )

