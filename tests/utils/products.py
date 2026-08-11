from models import Product
from seeds.products import products as product_data


def create_product(session, **kwargs):
    new_product = {
        "name": "Calabresa",
        "ingredients": ["Queijo"],
        "price": 50.0,
        "category": "Tradicional",
        "is_popular": True,
        "available": True
    }

    new_product.update(kwargs)

    product = Product(**new_product)

    session.add(product)
    session.commit()
    session.refresh(product)

    return product

def create_product_list(session):
    session.add_all(Product(**product) for product in product_data)
    session.commit()

    return