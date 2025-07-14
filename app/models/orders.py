from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class OrderItems(Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField("models.Order", related_name="orders_item")
    product = fields.ForeignKeyField("models.Product", related_name='orders_product')
    quantity = fields.SmallIntField()

GetOrderItems = pydantic_model_creator(OrderItems)
CreateOrderItems = pydantic_model_creator(OrderItems, name='OrderItemsIn',  exclude_readonly=True)


class Order(Model):
    id = fields.IntField(pk=True)
    partner = fields.ForeignKeyField("models.Partner", related_name="partners")
    comments = fields.TextField(null=True)
    total_amount = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    status = fields.BooleanField(default=False)

    items: fields.ReverseRelation["OrderItems"]

Tortoise.init_models(["app.models.orders",
                      "app.models.partners",
                      "app.models.category",
                      "app.models.products"], "models")
GetOrder = pydantic_model_creator(Order, name='Order')
CreateOrder = pydantic_model_creator(Order, name='OrderIn',  exclude_readonly=True, exclude=['total_amount', 'status'])
