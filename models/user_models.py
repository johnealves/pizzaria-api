from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, autoincrement=True, primary_key=True, index=True)
    name = Column("name", String(50), nullable=False)
    email = Column("email", String(100), nullable=False, unique=True)
    password = Column("password", String(100), nullable=False)
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)
    orders = relationship("Order", back_populates="user")
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
