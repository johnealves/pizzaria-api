from sqlalchemy import Boolean, Column, Integer, String

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, autoincrement=True, primary_key=True, index=True)
    name = Column("name", String(50), nullable=False)
    email = Column("email", String(100), nullable=False, unique=True)
    password = Column("password", String(100), nullable=False)
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin
