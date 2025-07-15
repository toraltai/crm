from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.warehouses import *
from ..models import Product, GetProduct


warehouseRouter = APIRouter()


@warehouseRouter.post("/add_warehouse", response_model = GetWarehouse)
async def create_warehouse(warehouse_obj: CreateWarehouse,): #type: ignore
    warehouse = await Warehouse.create(**warehouse_obj.dict(exclude_unset=True))
    return await GetWarehouse.from_tortoise_orm(warehouse)


""" Добавляет Товар для учета остатка! """
""" TODO Получение товара из редиса и инвалидация """
@warehouseRouter.post("/add")
async def create_stock(stock_obj: CreateStock): #type: ignore
    if await Product.get_or_none(id=stock_obj.product_id):
        product = await Stock.get_or_none(product=stock_obj.product_id)
        if product:
            return HTTPException(status_code=404,
                                 detail={"message":"Продукт уже в учёте"})
        else:
            stock = await Stock.create(**stock_obj.dict(exclude_unset=True))
            return await GetStock.from_tortoise_orm(stock)
    return HTTPException(status_code=404,
                         detail={"message":"Продукт не найден"})


@warehouseRouter.get("/list", response_model=List[GetStock])
async def full_stock():
    return await GetStock.from_queryset(Stock.all())