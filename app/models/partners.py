from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum


class Partner(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    category = fields.ForeignKeyField("models.Category", related_name="partners", null=True)
    address = fields.CharField(max_length=150)
    inn = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)


Tortoise.init_models(["app.models.partners",
                      "app.models.category"], "models")
GetPartner = pydantic_model_creator(Partner)
CreatePartner = pydantic_model_creator(Partner, name='PartnerIn',  exclude_readonly=True)