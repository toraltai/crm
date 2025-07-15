from fastapi import FastAPI, APIRouter
from app.router import api_router
from tortoise.contrib.fastapi import register_tortoise
from settings import *

import logging

""" для проверки запросов """
# logging.getLogger("aiosqlite").setLevel(logging.WARNING)
# logging.getLogger("asyncio").setLevel(logging.WARNING)

# # Включить только SQL-запросы Tortoise
# tortoise_logger = logging.getLogger("tortoise.db_client")
# tortoise_logger.setLevel(logging.DEBUG)

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="SQL >> %(message)s"
# )

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