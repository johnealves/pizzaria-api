from sqlalchemy.orm import Session
from models import Product
from fastapi import HTTPException, status

def get_product_by_id(product_id: int, session: Session):
    db_product = session.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found.")

    return db_product