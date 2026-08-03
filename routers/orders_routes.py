from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from db.dependency import get_session
from enums.order_status import OrderStatusEnum
from models import User
from schemas.order_schemas import (
    CreateOrderResponse,
    OrderSchema,
    ResponseOrdersSchema,
)
from security.auth import get_current_user
from services.order_service import OrderService

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(get_current_user)],
)


@orders_router.get("/", response_model=list[ResponseOrdersSchema])
async def list_orders(
    status_filter: OrderStatusEnum | None = Query(None),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return OrderService(session).list(status_filter, user)


@orders_router.get("/my", response_model=list[ResponseOrdersSchema])
async def my_orders(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return OrderService(session).list_by_user(user)


@orders_router.get("/{order_id}", response_model=ResponseOrdersSchema)
async def get_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return OrderService(session).get_by_id(order_id, user)


@orders_router.post(
    "/",
    response_model=CreateOrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    body: OrderSchema,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return OrderService(session).create(body, user)


@orders_router.patch("/{order_id}/status")
async def update_status(
    order_id: int,
    new_status: OrderStatusEnum,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return OrderService(session).update_status(order_id, new_status, user)


@orders_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return OrderService(session).cancel(order_id, user)
