from typing import Optional
from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum


class Type(Enum):
    litr = '1л',
    double = '0,5л',



class ProductPrice(Model):
    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField("models.Product", related_name="product_price")
    category = fields.ForeignKeyField("models.Category", related_name="category_price")
    price = fields.IntField()


GetProductPrice = pydantic_model_creator(ProductPrice)
CreateProductPrice = pydantic_model_creator(ProductPrice, name="ProductPriceIn", exclude_readonly=True)



class Product(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length = 50)
    
    attrs = fields.ManyToManyField(
        "models.ProductAttribute", related_name="products", through="attrs_product"
    )
    

    async def get_price_object(self, category_id: int) -> Optional[ProductPrice]:
        return await ProductPrice.get_or_none(
            product_id=self.id,
            category_id=category_id
        )

    async def get_price(self, category_id: int) -> Optional[int]:
        price_obj = await self.get_price_object(category_id)
        return price_obj.price if price_obj else None


GetProduct = pydantic_model_creator(Product)
CreateProduct = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)



class ProductAttribute(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    
    products: fields.ManyToManyRelation[Product]

GetProductAttribute = pydantic_model_creator(ProductAttribute)
CreateProductAttribute = pydantic_model_creator(ProductAttribute, name="ProductAttributeIn", exclude_readonly=True)