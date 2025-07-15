from pydantic import BaseModel
from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.validators import MinValueValidator
from tortoise.contrib.pydantic import pydantic_model_creator



class Warehouse(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(50)

GetWarehouse = pydantic_model_creator(Warehouse)
CreateWarehouse = pydantic_model_creator(Warehouse, name='WarehouseIn',  exclude_readonly=True)



class Stock(Model):
    id = fields.IntField(pk=True)
    warehouse = fields.ForeignKeyField("models.Warehouse", related_name='stocks')
    product = fields.ForeignKeyField("models.Product", related_name="stocks")
    quantity = fields.IntField(default=0)

Tortoise.init_models(["app.models.warehouses","app.models.products"], "models")
GetStock = pydantic_model_creator(Stock, exclude=("product.orders_product", "product.attrs", "product.product_price"))
CreateStock = pydantic_model_creator(Stock, name='StockIn', exclude_readonly=True, exclude=(["quantity"]))



class StockEntry(Model):
    pass
