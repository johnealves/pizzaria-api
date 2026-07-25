from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    user_id: int

    class Config:
        from_attributes = True

class ItemOrderSchema(BaseModel):
    quantity: int
    flavor: str
    amount: str
    unit_price: float

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attibutes = True

class ResponseOrdersSchema(BaseModel):
    id: int
    status: str
    price: float
    items: List[ItemOrderSchema]

    class Config:
        from_attributes = True