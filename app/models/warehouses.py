from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.validators import MinValueValidator
from tortoise.contrib.pydantic import pydantic_model_creator


# class Warehouse(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(50)


# GetWarehouse = pydantic_model_creator(Warehouse)
# CreateWarehouse = pydantic_model_creator(Warehouse, name='WarehouseIn',  exclude_readonly=True)


class Warehouse(Model):
    id = fields.IntField(pk=True)
    products = fields.ManyToManyField(
        "models.Product",
        related_name="stocks",
        through="stocks_product"  # опционально: имя таблицы-связки
    )
    quantity = fields.IntField()

Tortoise.init_models(["app.models.products"], "models")
GetWarehouse = pydantic_model_creator(Warehouse)
CreateWarehouse = pydantic_model_creator(Warehouse, name='WarehouseIn',  exclude_readonly=True)