from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.schemas.product import Product
from app.utils.config import get_config

if TYPE_CHECKING:
    from app.data_providers.csv_product_provider import CSVProductProvider


class ProductDataProvider(ABC):
    provider_name: str
    fallback_reason: str | None = None

    @abstractmethod
    def list_products(self, product_category: str | None = None) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    def get_product_by_id(self, product_id: str) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    def search_products(
        self,
        query: str,
        product_category: str | None = None,
        limit: int | None = None,
    ) -> list[Product]:
        raise NotImplementedError


def get_product_data_provider(provider_name: str | None = None) -> ProductDataProvider:
    from app.data_providers.csv_product_provider import CSVProductProvider

    requested = (provider_name or get_config().data_providers.product_provider).strip().lower()
    if requested == "csv":
        return CSVProductProvider()

    fallback_reason = (
        f"PRODUCT_PROVIDER={requested!r} is reserved or unsupported in the "
        "prototype; falling back to CSVProductProvider."
    )
    return CSVProductProvider(fallback_reason=fallback_reason)

