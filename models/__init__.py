from db.base import Base

from .order_models import Order, OrderItem
from .product_models import Product
from .user_models import User

__all__ = ["Base", "Order", "OrderItem", "User", "Product"]

# criar migração alembic revision --autogenerate -m "Mensagem da migratio"
# executar a migraçao: alembic upgrade head
