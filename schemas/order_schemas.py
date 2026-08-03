from pydantic import BaseModel

from enums.order_status import OrderStatusEnum
from schemas.user_schemas import UserInfo


class CreateOrderItemSchema(BaseModel):
    product_id: int
    quantity: int


class OrderSchema(BaseModel):
    user_id: int
    items: list[CreateOrderItemSchema]

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: OrderStatusEnum
    user: UserInfo


class CreateOrderResponse(BaseModel):
    message: str
    order: OrderResponse


class ItemOrderSchema(BaseModel):
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


class ResponseOrdersSchema(BaseModel):
    id: int
    status: str
    total_price: float
    items: list[ItemOrderSchema]

    class Config:
        from_attributes = True
