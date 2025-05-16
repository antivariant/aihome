# routers/log_routes.py
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import os
from datetime import datetime

from config.system_profiles import SYSTEM_PROFILES

router = APIRouter()
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://mongo:27017"))
db = client["frai"]

def serialize_log(log):
    log["_id"] = str(log["_id"])
    if isinstance(log.get("timestamp"), datetime):
        log["timestamp"] = log["timestamp"].isoformat()
    return log

@router.get("/human-log")
def get_human_log(interaction_id: str = Query(...)):
    logs = list(db["log_human"].find({"interaction_id": interaction_id}).sort("timestamp", 1))
    for log in logs:
        actor = log.get("actor")
        log["profile"] = SYSTEM_PROFILES.get(actor, {
            "name": actor,
            "avatar": "/avatars/default.png"
        })
    logs = [serialize_log(log) for log in logs]
    return JSONResponse(content=logs)
