from sqlalchemy.orm import Session

from models import Product
from .products import products

def seed_products(session: Session):
    if session.query(Product).count() > 0:
        print("Produtos ja cadastrado")
        return

    session.add_all(Product(**product) for product in products)
    session.commit()