from fastapi import APIRouter
from typing import List, Optional
from app.models.partners import *


partnerRouter = APIRouter()


@partnerRouter.post('/add', response_model = GetPartner)
async def create_partner(partner: CreatePartner): #type: ignore
    partner_obj = await Partner.create(**partner.dict(exclude_unset=True))
    return await GetPartner.from_tortoise_orm(partner_obj)


@partnerRouter.get('/list', response_model=List[GetPartner])
async def list():
    return await GetPartner.from_queryset(Partner.all().prefetch_related("category"))