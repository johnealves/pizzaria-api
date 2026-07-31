from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column("id", Integer, autoincrement=True, primary_key=True, index=True)
    name = Column("name", String, nullable=False)
    ingredients = Column("ingredients", JSON, nullable=False)
    price = Column("price", Float, nullable=False)
    category = Column("category", String, nullable=False)
    is_popular = Column("is_popular", Boolean, default=False)
    available = Column("available", Boolean, default=True)
    order_items = relationship("OrderItem", back_populates="product")
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
