import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')


APPS_MODEL = ['app.models']

DB_URL = "sqlite://db.sqlite3"
# DB_URL = f"asyncpg://postgres.fiyinaraapepwdztbbdi:{config('PASSWORD')}@aws-0-eu-north-1.pooler.supabase.com:5432/postgres"


CORS_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")