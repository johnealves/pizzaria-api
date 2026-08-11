from typing import List, Optional

from pydantic import BaseModel

from enums.product_category import ProductCategory


class ProductSchema(BaseModel):
    name: str
    ingredients: List[str]
    price: float
    category: Optional[ProductCategory] = ProductCategory.TRADITIONAL
    is_popular: Optional[bool] = False
    available: Optional[bool] = True

    class ConfigDict:
        from_attributes = True


class UpdateProductSchema(BaseModel):
    name: str | None = None
    ingredients: List[str] | None = None
    price: float | None = None
    category: ProductCategory | None = None
    is_popular: bool | None = None
    available: bool | None = None

    class ConfigDict:
        from_attribute = True


# Rersponse schemas
class ProductsResponse(BaseModel):
    id: int
    name: str
    ingredients: List[str]
    category: str
    is_popular: bool
    price: float
    available: bool

    class ConfigDict:
        from_attributes = True


class ProductsPageResponse(BaseModel):
    data: list[ProductsResponse]
    page: int
    limit: int
    total: int
    pages: int


class MessageResponse(BaseModel):
    message: str


class ProductActionResponse(BaseModel):
    message: str
    product: ProductsResponse
