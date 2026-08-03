from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from db.dependency import get_session
from models import User
from schemas.products_schemas import (
    ProductActionResponse,
    ProductSchema,
    ProductsPageResponse,
    ProductsResponse,
    UpdateProductSchema,
)
from security.auth import get_current_user
from services.product_service import ProductService

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/", response_model=ProductsPageResponse)
async def list_products(
    is_popular: bool | None = Query(None),
    available: bool | None = Query(None),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return ProductService(session).list(
        is_popular=is_popular,
        available=available,
        min_price=min_price,
        max_price=max_price,
        search=search,
        page=page,
        limit=limit,
    )


@products_router.get("/{product_id}", response_model=ProductsResponse)
async def get_product(product_id: int, session: Session = Depends(get_session)):
    return ProductService(session).get_product_by_id(product_id)


@products_router.post(
    "/", response_model=ProductActionResponse, status_code=status.HTTP_201_CREATED
)
async def create_product(
    body: ProductSchema,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return ProductService(session).create(body, user)


@products_router.patch("/{product_id}", response_model=ProductActionResponse)
async def update_product(
    product_id: int,
    body: UpdateProductSchema,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return ProductService(session).update(product_id, body, user)


@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return ProductService(session).delete(product_id, user)
