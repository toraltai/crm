from fastapi import APIRouter
from typing import List, Optional
from app.models.warehouses import *


warehouseRouter = APIRouter()


@warehouseRouter.post("/add")
async def create_warehouse(warehouse_obj: CreateWarehouse, #type: ignore
                           product_id: int):
    warehouse = await Warehouse.create(**warehouse_obj.dict(exclude_unset=True),
                                       product_id=product_id)
    return await GetWarehouse.from_tortoise_orm(warehouse)


@warehouseRouter.get("/list", response_model=List[GetWarehouse])
async def list():
    return await GetWarehouse.from_queryset(Warehouse.all())