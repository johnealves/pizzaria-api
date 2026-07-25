from enum import Enum


class OrderStatusEnum(str, Enum):
    PENDENTE = "PENDENTE"
    PREPARANDO = "PREPARANDO"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"
