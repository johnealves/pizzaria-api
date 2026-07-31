from enum import Enum


class ProductCategory(str, Enum):
    TRADITIONAL = "Tradicional"
    SWEET = "Doce"
    SPECIAL = "Especial"
    DRINK = "Bebida"
