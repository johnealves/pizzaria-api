from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, autoincrement=True, primary_key=True, index=True)
    status = Column("status", String, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column("total_price", Float, nullable=False)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")
    user = relationship("User", back_populates="orders")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    def count_price(self):
        self.total_price = sum(item.unit_price * item.quantity for item in self.items)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, autoincrement=True, primary_key=True, index=True)
    order_id = Column("order_id", Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(
        "product_id", Integer, ForeignKey("products.id"), nullable=False
    )
    quantity = Column("quantity", Integer, nullable=False)
    unit_price = Column("unit_price", Float, nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
