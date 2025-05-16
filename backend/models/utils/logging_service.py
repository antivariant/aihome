# services/logging_service.py
from datetime import datetime
import json
import os

from pymongo import MongoClient
import redis

from models.contracts.log.human_log_entry import HumanLogEntry
from models.contracts.log.tech_log_entry import TechLogEntry

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client["frai"]
human_log_collection = db["log_human"]
tech_log_collection = db["log_tech"]

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def log_human(entry: HumanLogEntry):
    redis_client.publish("human_logs", json.dumps(entry.dict(), default=json_serial))
    human_log_collection.insert_one(entry.dict())

def log_tech(entry: TechLogEntry):
    redis_client.publish("tech_logs", json.dumps(entry.dict(), default=json_serial))
    tech_log_collection.insert_one(entry.dict())
