from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.products import *


productRouter = APIRouter()


@productRouter.post("/add")
async def create_product(product: CreateProduct): #type: ignore
    product_obj = await Product.create(**product.dict(exclude_unset=True))
    return await GetProduct.from_tortoise_orm(product_obj)


@productRouter.get("/products-with-prices")
async def list_products_with_prices():
    products = await Product.all().prefetch_related("product_price__category")
    result = []

    for product in products:
        price_list = []
        for productPrice in product.product_price:
            price_list.append({
                "category": productPrice.category.title,
                "price": productPrice.price
            })

        result.append({
            "id": product.id,
            "title": product.title,
            "price": price_list
        })

    return result


@productRouter.post("/price/{id}", response_model = GetProductPrice)
async def put_price(price_data: CreateProductPrice,  #type: ignore
                         product_id: int,
                         category_id: int): 
    product_obj = await ProductPrice.create(**price_data.dict(exclude_unset=True),
                                       product_id = product_id,
                                       category_id = category_id)
    return await GetProductPrice.from_tortoise_orm(product_obj)