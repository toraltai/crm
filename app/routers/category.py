from fastapi import APIRouter
from typing import List, Optional
from app.models.category import *


categoryRouter = APIRouter()


@categoryRouter.post("/add")
async def create_category(cat: CreateCategory, #type: ignore
                          parent_id: Optional[int] = None):
    cat_obj = await Category.create(**cat.dict(exclude_unset=True),
                                    parent_id=parent_id)
    return await GetCategory.from_tortoise_orm(cat_obj)


@categoryRouter.get("/categories", response_model=List[GetCategory])
async def list():
    return await GetCategory.from_queryset(Category.all())