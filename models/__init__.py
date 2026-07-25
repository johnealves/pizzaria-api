from db.base import Base

from .order_models import Order, OrderItem
from .user_models import User

__all__ = ["Base", "Order", "OrderItem", "User"]

# criar migração alembic revision --autogenerate -m "Mensagem da migratio"
# executar a migraçao: alembic upgrade head
