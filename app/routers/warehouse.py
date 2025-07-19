from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.warehouses import *
from ..models import Product
from app.service.stock_service import StockService



warehouseRouter = APIRouter()



""" Оприходывание товара на складе """
@warehouseRouter.put("/add_quantity")
async def add_quantity(stock_obj: CreateStock, #type: ignore
                      quantity: int):
    
    stock = await Stock.get_or_none(product=stock_obj.product_id,
                                    warehouse_id=stock_obj.warehouse_id)

    if stock:
        new_quantity = stock.quantity + quantity
        await Stock.get(id=stock.id).update(**stock_obj.model_dump(exclude_unset=True),
                                            quantity=new_quantity)
        
        return await GetStock.from_queryset_single(Stock.get(id=stock.id))
    return HTTPException(status_code=404,
                                 detail={"message":"Продукт не найден"})



@warehouseRouter.post("/add_warehouse", response_model = GetWarehouse)
async def create_warehouse(warehouse_obj: CreateWarehouse,): #type: ignore
    warehouse = await Warehouse.create(**warehouse_obj.dict(exclude_unset=True))
    return await GetWarehouse.from_tortoise_orm(warehouse)



""" Добавляет Товар для учета остатка! """
""" TODO Получение товара из редиса и инвалидация """
@warehouseRouter.post("/add")
async def create_stock(stock_obj: CreateStock): #type: ignore
    stock = await Stock.filter(product_id=stock_obj.product_id,
                               warehouse_id = stock_obj.warehouse_id).first()
    
    if stock:
        return HTTPException(status_code=404,
                             detail={"message":"Продукт уже в учёте"})
    
    stock = await Stock.create(**stock_obj.dict(exclude_unset=True))
    return await GetStock.from_tortoise_orm(stock)  



@warehouseRouter.get("/list", response_model=List[GetStock])
async def full_stock():
    return await GetStock.from_queryset(Stock.all())



@warehouseRouter.post("/")
async def transfer(obj_: CreateStockTransfer, #type: ignore
                   from_warehouse: int,
                   to_warehouse: int):
    
    transfer_obj = await StockTransfer.create(**obj_.dict(exclude_unset=True),
                                              from_warehouse_id=from_warehouse,
                                              to_warehouse_id=to_warehouse)
    
    return await GetStockTransfer.from_tortoise_orm(transfer_obj)



""" Перемещение """
@warehouseRouter.post("/transfer")
async def transfer_items(transfer_id: int, items: List[TransferItem]):
    return await StockService.transfer_bulk(transfer_id, items)