from fastapi import APIRouter
from .routers.category import categoryRouter
from .routers.partner import partnerRouter
from .routers.product import productRouter
from .routers.order import orderRouter
from .routers.warehouse import warehouseRouter


api_router = APIRouter()


api_router.include_router(categoryRouter, prefix='/category', tags=['Category API'])
api_router.include_router(partnerRouter, prefix='/partner', tags=['Partner API'])
api_router.include_router(orderRouter, prefix='/order', tags=['Order API'])
api_router.include_router(productRouter, prefix='/product', tags=['Product API'])
# api_router.include_router(warehouseRouter, prefix='/warehouse', tags=['Warehouse API'])