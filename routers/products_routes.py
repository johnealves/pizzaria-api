from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.dependency import get_session
from models import Product, User
from schemas.products_schemas import (
    ProductsResponse,
    ProductSchema,
    UpdateProductSchema,
    ProductActionResponse
)
from security.auth import get_current_user

products_router = APIRouter(prefix="/products", tags=["Products"])

def get_product_by_id(
    product_id: int,
    session: Session
):
    db_product = session.query(Product).filter(Product.id == product_id).first()

    if not db_product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found.")

    return db_product


@products_router.get("/", response_model=list[ProductsResponse])
async def list_products(
    is_popular: bool | None = Query(None),
    available: bool | None = Query(None),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    query = session.query(Product)
    
    if is_popular is not None:
        query = query.filter(Product.is_popular == is_popular)

    if available is not None:
        query = query.filter(Product.available == available)
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%")) 

    total = query.count()

    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    return {
        "data": query.all(),
        "page": page,
        "limit": limit,
        "total": total,
        "pages": ceil(total / limit)
    }

@products_router.get("/{product_id}", response_model=ProductsResponse)
async def get_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = get_product_by_id(product_id, session)

    return product

@products_router.post("/", response_model=ProductActionResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    add_product: ProductSchema,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    if not user.admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User is not authorized.")
    
    existing_product = session.query(Product).filter(Product.name == add_product.name).first()

    if existing_product:
        raise HTTPException(status.HTTP_409_CONFLICT, "Product already exists.")

    new_product = Product(**add_product.model_dump())

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return {
        "message": "Product created successfully.",
        "product": new_product
    }

@products_router.patch("/{product_id}", response_model=ProductActionResponse)
async def update_product(
    product_id: int,
    update_body: UpdateProductSchema,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    if not user.admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User is not authorized.")
    
    db_product = get_product_by_id(product_id, session)

    update_data = update_body.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_product, key, value)

    session.commit()
    session.refresh(db_product)

    return {
        "message": "Product updated successfully.",
        "product": db_product
    }

@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    if not user.admin:
            raise HTTPException(403, "User is not authorized.")
    
    db_product = get_product_by_id(product_id, session)

    session.delete(db_product)
    session.commit()

    return
