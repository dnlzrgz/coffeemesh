from datetime import datetime
import uuid
from uuid import UUID

from fastapi import status, HTTPException
from fastapi.responses import Response

from orders.app import app
from orders.api.schemas import (
    Status,
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
)

orders = []


@app.get("/orders", response_model=GetOrdersSchema)
def get_orders():
    return {"orders": orders}


@app.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(order_details: CreateOrderSchema):
    order = order_details.model_dump()
    order["id"] = uuid.uuid4()
    order["created"] = datetime.utcnow()
    order["status"] = Status.created
    orders.append(order)

    return order


@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            return order

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )


@app.put("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in orders:
        if order["id"] == order_id:
            order.update(order_details.model_dump())
            return order

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )


@app.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_order(order_id: UUID):
    for index, order in enumerate(orders):
        if order["id"] == order_id:
            orders.pop(index)
            return

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )


@app.post(
    "/orders/{order_id}/cancel",
    response_model=GetOrderSchema,
)
def cancel_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = Status.cancelled
            return order

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )


@app.post(
    "/orders/{order_id}/pay",
    response_model=GetOrderSchema,
)
def pay_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = Status.cancelled
            return order

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )
