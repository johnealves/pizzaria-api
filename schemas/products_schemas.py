from typing import List, Optional

from pydantic import BaseModel

class ProductSchema(BaseModel):
    name: str
    ingredients: List[str]
    price: float
    is_popular: Optional[bool] = False
    available: Optional[bool] = True

    class Config:
        from_attributes = True

class UpdateProductSchema(BaseModel):
    name: str | None = None
    ingredients: List[str] | None = None
    price: float | None = None
    is_popular: bool | None = None
    available: bool | None = None

# Rersponse schemas
class ProductsResponse(BaseModel):
    id: int
    name: str
    ingredients: List[str]
    is_popular: bool
    price: float
    available: bool

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str

class ProductActionResponse(BaseModel):
    message: str
    product: ProductsResponse