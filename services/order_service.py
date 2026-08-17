from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from enums.order_status import OrderStatusEnum
from models import Order, OrderItem, User
from schemas.order_schemas import (
    CreateOrderResponse,
    OrderSchema,
)
from services.product_service import ProductService


class OrderService:
    def __init__(self, session: Session):
        self.session = session

    def _validate_admin(self, user: User):
        if not user.admin:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "User is not authorized.",
            )

    def get_order_by_id(self, order_id: int) -> Order:
        order = self.session.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Order not found.",
            )

        return order

    def list(
        self,
        status_filter: OrderStatusEnum | None,
        user: User,
    ):
        self._validate_admin(user)

        query = self.session.query(Order)

        if status_filter:
            query = query.filter(Order.status == status_filter)

        return query.all()

    def list_by_user(self, user: User):
        return self.session.query(Order).filter(Order.user_id == user.id).all()

    def get_by_id(
        self,
        order_id: int,
        user: User,
    ):
        order = self.get_order_by_id(order_id)

        if not user.admin and order.user_id != user.id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "User is not authorized.",
            )

        return order

    def create(
        self,
        body: OrderSchema,
        user: User,
    ) -> CreateOrderResponse:

        order = Order(
            user_id=body.user_id,
            status=OrderStatusEnum.PENDENTE,
            total_price=0,
        )

        try:
            self.session.add(order)
            self.session.flush()

            total = 0

            for item in body.items:
                product = ProductService(self.session).get_product_by_id(
                    item.product_id
                )

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=product.price,
                )

                total += order_item.quantity * order_item.unit_price

                self.session.add(order_item)

            order.total_price = total

            self.session.commit()
            self.session.refresh(order)

            return {
                "message": "Order created successfully.",
                "order": order,
            }

        except Exception:
            self.session.rollback()
            raise

    def update_status(
        self,
        order_id: int,
        new_status: OrderStatusEnum,
        user: User,
    ):
        self._validate_admin(user)

        order = self.get_order_by_id(order_id)

        try:
            order.status = new_status

            self.session.commit()
            self.session.refresh(order)

            return {
                "message": "Order status updated successfully.",
                "order": order,
            }

        except Exception:
            self.session.rollback()
            raise

    def cancel(
        self,
        order_id: int,
        user: User,
    ):
        order = self.get_order_by_id(order_id)

        if not user.admin and order.user_id != user.id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "User is not authorized.",
            )

        try:
            order.status = OrderStatusEnum.CANCELADO

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise
