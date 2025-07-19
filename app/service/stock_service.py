from fastapi import HTTPException
from typing import List, Optional
from tortoise.transactions import in_transaction

from app.models.warehouses import *



class StockService:
    @classmethod
    async def transfer_bulk(cls,
                            transfer_id: int,
                            from_warehouse: Optional[int],
                            to_warehouse: Optional[int],
                            items: List[TransferItem]):
        
        transfer = await StockTransfer.get(id=transfer_id)
        if not transfer:
            raise HTTPException(status_code=404, detail="Перемещение не найдено")

        transfer_items = []

        for item in items:
            product_id = item.product_id
            quantity = item.quantity

            from_stock = await Stock.filter(
                warehouse_id=transfer.from_warehouse_id,
                product_id=product_id
            ).first()

            if not from_stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Товар не найден на складе отправителе")

            if from_stock.quantity < quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Недостаточно товара на складе")

            to_stock = await Stock.get_or_none(
                warehouse_id=transfer.to_warehouse_id,
                product_id=product_id)

            if to_stock:
                to_stock.quantity += quantity
                await to_stock.save()
            else:
                await Stock.create(
                    warehouse_id=transfer.to_warehouse_id,
                    product_id=product_id,
                    quantity=quantity)

            from_stock.quantity -= quantity
            await from_stock.save()

            transfer_items.append(
                StockTransferItem(
                    transfer_id=transfer_id,
                    product_id=product_id,
                    quantity=quantity
                )
            )

        await StockTransferItem.bulk_create(transfer_items)

        return {"message": "Перемещение завершено"}