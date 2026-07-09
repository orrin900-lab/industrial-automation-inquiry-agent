from app.data_providers import (
    CSVProductProvider,
    DatabaseProductProvider,
    ERPProductProvider,
    ProductDataProvider,
    get_product_data_provider,
)
from app.utils.config import get_config


def test_csv_product_provider_reads_products_csv():
    provider: ProductDataProvider = CSVProductProvider()

    products = provider.list_products()

    assert products
    assert products[0].product_id
    assert products[0].product_name


def test_csv_product_provider_get_product_by_id_and_search():
    provider = CSVProductProvider()
    first = provider.list_products()[0]

    loaded = provider.get_product_by_id(first.product_id)
    results = provider.search_products(
        query=f"{first.product_name} {first.model or ''}",
        product_category=first.category,
        limit=5,
    )

    assert loaded is not None
    assert loaded.product_id == first.product_id
    assert any(product.product_id == first.product_id for product in results)


def test_product_provider_factory_defaults_to_csv(monkeypatch):
    monkeypatch.setenv("PRODUCT_PROVIDER", "csv")
    get_config.cache_clear()

    provider = get_product_data_provider()

    assert isinstance(provider, CSVProductProvider)
    assert provider.fallback_reason is None


def test_reserved_product_provider_falls_back_to_csv_with_reason(monkeypatch):
    monkeypatch.setenv("PRODUCT_PROVIDER", "erp")
    get_config.cache_clear()

    provider = get_product_data_provider()

    assert isinstance(provider, CSVProductProvider)
    assert provider.provider_name == "csv"
    assert provider.fallback_reason
    assert "falling back" in provider.fallback_reason


def test_reserved_provider_classes_are_explicit_skeletons():
    database_provider = DatabaseProductProvider()
    erp_provider = ERPProductProvider()

    for provider in [database_provider, erp_provider]:
        try:
            provider.list_products()
        except NotImplementedError as exc:
            assert "reserved" in str(exc).lower()
        else:
            raise AssertionError("Reserved provider should raise NotImplementedError.")

