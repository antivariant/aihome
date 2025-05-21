import os, time, uuid, shutil
from pymongo import MongoClient
from datetime import datetime
import httpx

API_TOKEN   = os.getenv("CHAT_API_TOKEN")
GW_HUB_URL  = os.getenv("GW_HUB_URL")
UPLOAD_DIR  = "/app/uploads"
MONGO_URI   = os.getenv("MONGODB_URI", "mongodb://mongo:27017")

# инициализируем БД один раз
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["frai"]
uploads_col = db["chat_uploads"]

# helper для HTTP-клиента
async def get_hub_client():
    async with httpx.AsyncClient() as client:
        yield client
