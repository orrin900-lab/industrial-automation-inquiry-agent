from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db.models import ProductRecord
from app.schemas.product import Product


class ProductLibraryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def count(self) -> int:
        return len(self.db.execute(select(ProductRecord.id)).all())

    def upsert_from_product(self, product: Product, *, is_active: bool = True) -> ProductRecord:
        record = self.get_by_product_id(product.product_id)
        payload = product.model_dump(mode="json")
        if record is None:
            record = ProductRecord(
                product_id=product.product_id,
                product_name=product.product_name,
                category=product.category,
                brand=product.brand,
                model=product.model,
                is_active=is_active,
                product_json=payload,
            )
            self.db.add(record)
        else:
            record.product_name = product.product_name
            record.category = product.category
            record.brand = product.brand
            record.model = product.model
            record.product_json = payload
        self.db.flush()
        return record

    def create_or_replace(self, product: Product, *, is_active: bool = True) -> ProductRecord:
        record = self.upsert_from_product(product, is_active=is_active)
        record.is_active = is_active
        self.db.add(record)
        self.db.flush()
        return record

    def get_by_product_id(self, product_id: str) -> ProductRecord | None:
        stmt = select(ProductRecord).where(ProductRecord.product_id == product_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        *,
        category: str | None = None,
        query: str | None = None,
        active_only: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[ProductRecord], int]:
        stmt: Select = select(ProductRecord)
        count_stmt: Select = select(ProductRecord.id)
        if category:
            stmt = stmt.where(ProductRecord.category == category)
            count_stmt = count_stmt.where(ProductRecord.category == category)
        if active_only:
            stmt = stmt.where(ProductRecord.is_active.is_(True))
            count_stmt = count_stmt.where(ProductRecord.is_active.is_(True))
        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(
                ProductRecord.product_name.ilike(pattern)
                | ProductRecord.product_id.ilike(pattern)
                | ProductRecord.model.ilike(pattern)
                | ProductRecord.brand.ilike(pattern)
            )
            count_stmt = count_stmt.where(
                ProductRecord.product_name.ilike(pattern)
                | ProductRecord.product_id.ilike(pattern)
                | ProductRecord.model.ilike(pattern)
                | ProductRecord.brand.ilike(pattern)
            )

        total = len(self.db.execute(count_stmt).all())
        rows = self.db.execute(
            stmt.order_by(ProductRecord.category, ProductRecord.product_id)
            .limit(limit)
            .offset(offset)
        ).scalars().all()
        return list(rows), total


def product_record_to_dict(record: ProductRecord) -> dict:
    product = Product(**record.product_json)
    return {
        "product_id": record.product_id,
        "product_name": record.product_name,
        "category": record.category,
        "brand": record.brand,
        "model": record.model,
        "is_active": record.is_active,
        "product": product.model_dump(mode="json"),
    }
