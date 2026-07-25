from db.base import Base

from .user_models import User
from .order_models import Order, OrderItem

__all__ = ["Base", "User", "Order", "OrderItem"]

# criar migração alembic revision --autogenerate -m "Mensagem da migratio"
# executar a migraçao: alembic upgrade head