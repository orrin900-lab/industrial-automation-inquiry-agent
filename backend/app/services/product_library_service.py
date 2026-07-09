from sqlalchemy.orm import Session

from app.data_providers.csv_product_provider import CSVProductProvider
from app.repositories.product_library_repository import (
    ProductLibraryRepository,
    product_record_to_dict,
)
from app.schemas.product import Product, ProductLibraryCreate, ProductLibraryUpdate


PROVIDER_NOTE = (
    "Product Library Admin uses a demo PostgreSQL product table seeded from "
    "products.csv. Agent matching still defaults to CSVProductProvider for stable "
    "prototype behavior."
)


def ensure_seeded_from_csv(db: Session) -> None:
    repo = ProductLibraryRepository(db)
    if repo.count() > 0:
        return
    for product in CSVProductProvider().list_products():
        repo.upsert_from_product(product)
    db.commit()


def list_product_library(
    db: Session,
    *,
    category: str | None = None,
    query: str | None = None,
    active_only: bool = False,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    ensure_seeded_from_csv(db)
    rows, total = ProductLibraryRepository(db).list(
        category=category,
        query=query,
        active_only=active_only,
        limit=limit,
        offset=offset,
    )
    return {
        "status": "success",
        "items": [product_record_to_dict(record) for record in rows],
        "total": total,
        "provider_note": PROVIDER_NOTE,
    }


def get_product_library_item(db: Session, product_id: str) -> dict | None:
    ensure_seeded_from_csv(db)
    record = ProductLibraryRepository(db).get_by_product_id(product_id)
    if record is None:
        return None
    return product_record_to_dict(record)


def create_product_library_item(db: Session, payload: ProductLibraryCreate) -> dict:
    product = Product(**payload.model_dump(exclude={"is_active"}))
    record = ProductLibraryRepository(db).create_or_replace(
        product,
        is_active=payload.is_active,
    )
    db.commit()
    db.refresh(record)
    return product_record_to_dict(record)


def update_product_library_item(
    db: Session,
    product_id: str,
    payload: ProductLibraryUpdate,
) -> dict | None:
    ensure_seeded_from_csv(db)
    repo = ProductLibraryRepository(db)
    record = repo.get_by_product_id(product_id)
    if record is None:
        return None

    product_data = dict(record.product_json)
    if payload.product_data:
        product_data.update(payload.product_data)
    for field in ["product_name", "category", "brand", "model"]:
        value = getattr(payload, field)
        if value is not None:
            product_data[field] = value

    product_data["product_id"] = product_id
    product = Product(**product_data)
    record.product_name = product.product_name
    record.category = product.category
    record.brand = product.brand
    record.model = product.model
    record.product_json = product.model_dump(mode="json")
    if payload.is_active is not None:
        record.is_active = payload.is_active
    db.add(record)
    db.commit()
    db.refresh(record)
    return product_record_to_dict(record)


def set_product_active(db: Session, product_id: str, is_active: bool) -> dict | None:
    ensure_seeded_from_csv(db)
    record = ProductLibraryRepository(db).get_by_product_id(product_id)
    if record is None:
        return None
    record.is_active = is_active
    db.add(record)
    db.commit()
    db.refresh(record)
    return product_record_to_dict(record)
