from fastapi import FastAPI, APIRouter
from app.router import api_router
from tortoise.contrib.fastapi import register_tortoise
from settings import *


app = FastAPI(title="Organic CRM")


app.include_router(api_router, prefix='/api/v1')


@app.get('/')
async def home():
    return {"status":"good"}


register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": APPS_MODEL},
    generate_schemas=True,
    add_exception_handlers=True
)