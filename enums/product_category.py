from enum import Enum


class ProductCategory(str, Enum):
    TRADITIONAL = "TRADITIONAL"
    SWEET = "SWEET"
    SPECIAL = "SPECIAL"
    DRINK = "DRINK"
