from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from core.exceptions import ProductNotFoundException
from models import Product, User
from schemas.products_schemas import (
    ProductActionResponse,
    ProductSchema,
    ProductsPageResponse,
    ProductsResponse,
    UpdateProductSchema,
)


class ProductService:
    def __init__(self, session: Session):
        self.session = session

    def _validate_admin(self, user: User):
        if not user.admin:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "User is not authorized.")

    def get_product_by_id(self, product_id: int) -> ProductsResponse:
        db_product = (
            self.session.query(Product).filter(Product.id == product_id).first()
        )

        if not db_product:
            raise ProductNotFoundException()

        return db_product

    def get_product_by_name(self, name: str) -> Product | None:
        return (
            self.session.query(Product)
            .filter(func.lower(Product.name) == name.strip().lower())
            .first()
        )

    def create(self, body: ProductSchema, user: User) -> ProductActionResponse:
        try:
            self._validate_admin(user)

            product = self.get_product_by_name(body.name)

            if product:
                raise HTTPException(status.HTTP_409_CONFLICT, "Product already exists.")

            created_product = Product(**body.model_dump())

            self.session.add(created_product)
            self.session.commit()
            self.session.refresh(created_product)

            return {
                "message": "Product created successfully.",
                "product": created_product,
            }
        except Exception:
            self.session.rollback()
            raise

    def list(
        self,
        is_popular: bool | None = None,
        available: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> ProductsPageResponse:
        query = self.session.query(Product)

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

        products = query.offset((page - 1) * limit).limit(limit).all()

        return {
            "data": products,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": ceil(total / limit),
        }

    def update(
        self, product_id: int, body: UpdateProductSchema, user: User
    ) -> ProductActionResponse:
        self._validate_admin(user)

        try:
            db_product = self.get_product_by_id(product_id)
            if body.name is not None:
                product = self.get_product_by_name(body.name)

                if product and product.id != product_id:
                    raise HTTPException(
                        status.HTTP_409_CONFLICT, "Product name already used."
                    )

            update_data = body.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(db_product, key, value)

            self.session.commit()
            self.session.refresh(db_product)

            return {"message": "Product updated successfully.", "product": db_product}
        except Exception:
            self.session.rollback()
            raise

    def delete(self, product_id: int, user: User):
        try:
            self._validate_admin(user)

            db_product = self.get_product_by_id(product_id)

            self.session.delete(db_product)
            self.session.commit()

            return
        except Exception:
            self.session.rollback()
            raise
