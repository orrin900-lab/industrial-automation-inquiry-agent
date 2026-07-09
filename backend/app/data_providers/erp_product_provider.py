from app.data_providers.product_provider import ProductDataProvider
from app.schemas.product import Product


class ERPProductProvider(ProductDataProvider):
    provider_name = "erp"

    def list_products(self, product_category: str | None = None) -> list[Product]:
        raise NotImplementedError(
            "ERPProductProvider is reserved for future SAP/Kingdee/Yonyou/internal ERP integration."
        )

    def get_product_by_id(self, product_id: str) -> Product | None:
        raise NotImplementedError(
            "ERPProductProvider is reserved for future SAP/Kingdee/Yonyou/internal ERP integration."
        )

    def search_products(
        self,
        query: str,
        product_category: str | None = None,
        limit: int | None = None,
    ) -> list[Product]:
        raise NotImplementedError(
            "ERPProductProvider is reserved for future SAP/Kingdee/Yonyou/internal ERP integration."
        )

