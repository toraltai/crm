from fastapi import HTTPException
from tortoise.transactions import in_transaction

from app.models.orders import *
from app.models.products import *


class OrderService:
    @classmethod
    async def add_item_to_order(cls,
                                order_obj: CreateOrderItems, #type: ignore
                                order_id: int,
                                product_id: int,
                                ):
        async with in_transaction() as connection:
            order = await Order.get(id=order_id).prefetch_related("partner__category")
            product_price = await ProductPrice.get(product_id=product_id,
                                                    category=order.partner.category)

            item = await OrderItems.get_or_none(order_id=order_id,
                                                product_id=product_id)
            
            if item:
                item.quantity += order_obj.quantity
                await item.save(using_db=connection)
            else:
                item = await OrderItems.create(
                    order_id=order_id,
                    product_id=product_id,
                    quantity=order_obj.quantity
                )
                
            order.total_amount += order_obj.quantity * product_price.price
            await order.save(using_db=connection)
            
            return await GetOrderItems.from_tortoise_orm(item)