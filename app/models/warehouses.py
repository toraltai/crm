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



class StockTransfer(Model):
    id = fields.IntField(pk=True)
    from_warehouse = fields.ForeignKeyField("models.Warehouse", related_name="outgoing_transfers")
    to_warehouse = fields.ForeignKeyField("models.Warehouse", related_name="incoming_transfers")
    transfer_date = fields.DatetimeField(auto_now_add=True)
    comment = fields.TextField(null=True)

GetStockTransfer = pydantic_model_creator(StockTransfer)
CreateStockTransfer = pydantic_model_creator(StockTransfer, name="StockTransferIn", exclude_readonly=True)



class TransferItem(BaseModel):
    product_id: int
    quantity: int



class StockTransferItem(Model):
    id = fields.IntField(pk=True)
    transfer = fields.ForeignKeyField("models.StockTransfer", related_name="items")
    product = fields.ForeignKeyField("models.Product", related_name="transfer_items")
    quantity = fields.IntField()

GetStockTransferItem = pydantic_model_creator(StockTransferItem)
CreateStockTransferItem = pydantic_model_creator(StockTransferItem, name="StockTransferItemIn", exclude_readonly=True)