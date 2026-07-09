from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.db.session import get_db
from app.schemas.product import (
    ProductLibraryCreate,
    ProductLibraryUpdate,
    ProductStatusUpdate,
)
from app.services.product_library_service import (
    create_product_library_item,
    get_product_library_item,
    list_product_library,
    set_product_active,
    update_product_library_item,
)


router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(require_roles("admin"))],
)


@router.get("")
def list_products_endpoint(
    category: str | None = None,
    query: str | None = None,
    active_only: bool = False,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: Session = Depends(get_db),
) -> dict:
    return list_product_library(
        db,
        category=category,
        query=query,
        active_only=active_only,
        limit=limit,
        offset=offset,
    )


@router.get("/{product_id}")
def get_product_endpoint(product_id: str, db: Session = Depends(get_db)) -> dict:
    product = get_product_library_item(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product


@router.post("")
def create_product_endpoint(
    payload: ProductLibraryCreate,
    db: Session = Depends(get_db),
) -> dict:
    return {
        "status": "success",
        "product": create_product_library_item(db, payload),
    }


@router.patch("/{product_id}")
def update_product_endpoint(
    product_id: str,
    payload: ProductLibraryUpdate,
    db: Session = Depends(get_db),
) -> dict:
    product = update_product_library_item(db, product_id, payload)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    return {
        "status": "success",
        "product": product,
    }


@router.patch("/{product_id}/status")
def update_product_status_endpoint(
    product_id: str,
    payload: ProductStatusUpdate,
    db: Session = Depends(get_db),
) -> dict:
    product = set_product_active(db, product_id, payload.is_active)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    return {
        "status": "success",
        "product": product,
    }
