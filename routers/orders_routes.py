from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.dependency import get_session
from enums.order_status import OrderStatusEnum
from models import Order, OrderItem, User, Product
from schemas.schemas import ItemOrderSchema, ResponseOrdersSchema
from schemas.order_schemas import OrderSchema, CreateOrderResponse
from security.auth import get_current_user
from services.product_services import get_product_by_id

orders_router = APIRouter(
    prefix="/orders", tags=["orders"], dependencies=[Depends(get_current_user)]
)


@orders_router.get("/")
async def list_orders(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    if not user.admin:
        raise HTTPException(
            status_code=401, detail="User don't have authorization to view orders"
        )
    else:
        orders = session.query(Order).all()
        return {"orders": orders}


@orders_router.get("/my", response_model=list[ResponseOrdersSchema])
async def get_order_by_user(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    orders = session.query(Order).filter(Order.user_id == user.id).all()

    return orders


@orders_router.get("/{order_id}")
async def get_order_by_id(
    order_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    order: Order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and order.user_id != user.id:
        raise HTTPException(status_code=401, detail="Not authorized")

    return {"order": order, "items_quantity": len(order.items)}


@orders_router.post("/", response_model=CreateOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(new_order: OrderSchema, session: Session = Depends(get_session)):
    order = Order(
        user_id=new_order.user_id,
        status=OrderStatusEnum.PENDENTE,
        total_price=0
    )
    session.add(order)
    session.flush()

    total = 0
    for item in new_order.item:
        product = get_product_by_id(item.product_id, session)

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price
        )

        total += order_item.quantity * order_item.unit_price
        session.add(order_item)

    order.total_price = total

    session.commit()
    session.refresh(order)
    return {
        "message": "Order created successfully",
        "order": order
    }

@orders_router.post("/add-item/{order_id}")
async def add_item_order(
    order_id: str,
    item_order_schema: ItemOrderSchema,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    order = session.query(Order).filter(order_id == Order.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="User not authorized.")

    item_order = OrderItem(
        item_order_schema.quantity,
        item_order_schema.flavor,
        item_order_schema.amount,
        item_order_schema.unit_price,
        order_id,
    )

    session.add(item_order)
    order.count_price()
    session.commit()

    return {
        "message": "Item added to order successfully",
        "item_id": item_order.id,
        "order_price": order.price,
    }


@orders_router.post("/remove-item/{item_order_id}")
async def remove_item_order(
    item_order_id: str,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    item_order = session.query(OrderItem).filter(item_order_id == OrderItem.id).first()
    order = session.query(Order).filter(item_order.order_id == Order.id).first()
    if not item_order:
        raise HTTPException(status_code=404, detail="Item not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="User not authorized.")

    session.delete(item_order)
    order.count_price()
    session.commit()

    return {
        "message": "Item removed from order successfully",
        "total_price": order.price,
        "order": order,
    }


@orders_router.patch("/status/{order_id}")
async def update_order(
    order_id: int,
    new_status: OrderStatusEnum,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    selected_order: Order = session.query(Order).filter(Order.id == order_id).first()
    if not selected_order:
        raise HTTPException(status_code=404, detail="order not found")
    if not user.admin and user.id != selected_order.user_id:
        raise HTTPException(
            status_code=401, detail="User don't have authorization edit this order"
        )

    selected_order.status = new_status.upper()
    session.commit()
    return {
        "mensagem": f"Order No. {selected_order.id} has been updated.",
        "pedido": selected_order,
    }
