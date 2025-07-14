from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class Category(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=25)
    parent: fields.ForeignKeyNullableRelation['Category'] = fields.ForeignKeyField(
        'models.Category', on_delete=fields.CASCADE, null=True, related_name='children'
    )
    children: fields.ReverseRelation["Category"]

    def __str__(self):
        return self.title
    
    class PydanticMeta:
        backward_relations = False
        allow_cycles = True
        max_recursion = 3

Tortoise.init_models(["app.models.category"], "models")
""" Tortoise.init_models() инициализирует серализацию модели, для вывода связей """
GetCategory = pydantic_model_creator(Category)
CreateCategory = pydantic_model_creator(Category, name='CategoryIn',  exclude_readonly=True, exclude=['parent_id'])