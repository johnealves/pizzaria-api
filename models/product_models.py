from sqlalchemy import Column, Integer, String, Float, Boolean, JSON

from db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column("id", Integer, autoincrement=True, primary_key=True, index=True)
    name = Column("name", String, nullable=False)
    ingredients = Column("ingredients", JSON, nullable=False)
    is_popular = Column("is_popular", Boolean, default=False)
    price = Column("price", Float, nullable=False)
    available = Column("available", Boolean, default=True)