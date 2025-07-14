from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.service.order_service import *
from app.models.orders import *
from app.models.products import *


orderRouter = APIRouter()


@orderRouter.post('/add', response_model=GetOrder)
async def create_order(order: CreateOrder,): #type: ignore
    order_obj = await Order.create(**order.dict(exclude_unset=True),

                            )
    return await GetOrder.from_tortoise_orm(order_obj)


@orderRouter.get("/list", response_model=List[GetOrder])
async def list():
    return await GetOrder.from_queryset(Order.all().prefetch_related('partner'))


@orderRouter.post('/order-item', response_model=GetOrderItems)
async def add_item_to_order(order_obj: CreateOrderItems,  # type: ignore
                            order_id: int,
                            product_id: int,):
    return await OrderService.add_item_to_order(order_obj, order_id, product_id)

