from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, autoincrement=True, primary_key=True, index=True)
    status = Column("status", String, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    price = Column("price", Float, nullable=False)
    items = relationship("OrderItem", cascade="all, delete")

    def __init__(self, status, user_id, price):
        self.status = status
        self.user_id = user_id
        self.price = price

    def count_price(self):
        self.price = sum(item.unit_price * item.quantity for item in self.items)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, autoincrement=True, primary_key=True, index=True)
    quantity = Column("quantity", Integer, nullable=False)
    flavor = Column("flavor", String, nullable=False)
    amount = Column("amount", Integer, nullable=False)
    unit_price = Column("unit_price", Float, nullable=False)
    order_id = Column("order_id", Integer, ForeignKey("orders.id"), nullable=False)


    def __init__(self, quantity, flavor, amount, unit_price, order_id):
        self.quantity = quantity
        self.flavor = flavor
        self.amount = amount
        self.unit_price = unit_price
        self.order_id = order_id