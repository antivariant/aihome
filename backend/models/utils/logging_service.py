# services/logging_service.py
from datetime import datetime
import json
import os

from pymongo import MongoClient
import redis

from models.contracts.log.human_log_entry import HumanLogEntry
from models.contracts.log.tech_log_entry import TechLogEntry

# Настройки Redis для публикации логов
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Настройки MongoDB для хранения логов
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client["frai"]
human_log_collection = db["log_human"]
tech_log_collection = db["log_tech"]

def json_serial(obj):
    """
    Сериализация объектов datetime в ISO-формат для JSON
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def log_human(entry: HumanLogEntry):
    """
    Публикует human-лог в Redis и сохраняет в MongoDB
    """
    payload = json.dumps(entry.dict(), default=json_serial)
    redis_client.publish("human_logs", payload)
    human_log_collection.insert_one(entry.dict())


def log_tech(entry: TechLogEntry):
    """
    Публикует tech-лог в Redis и сохраняет в MongoDB
    """
    payload = json.dumps(entry.dict(), default=json_serial)
    redis_client.publish("tech_logs", payload)
    tech_log_collection.insert_one(entry.dict())


# ----------------------------------------------------------------
# Утилитарные фабрики логгеров для упрощённого вызова в модулях

def make_human_logger(actor: str, session_id: str, interaction_id: str):
    """
    Возвращает функцию hlog(message: str, target: str), которая сама дополняет
    timestamp, actor, target, session_id и interaction_id.

    Пример использования:
        hlog = make_human_logger("gw-chat", sid, iid)
        hlog("Сообщение", "gw-hub")
    """
    def hlog(message: str, target: str):
        entry = HumanLogEntry(
            timestamp=datetime.now(),
            actor=actor,
            target=target,
            message=message,
            session_id=session_id,
            interaction_id=interaction_id
        )
        log_human(entry)
    return hlog


def make_tech_logger(service: str, session_id: str, interaction_id: str):
    """
    Возвращает функцию tlog(level: str, **data), которая сама дополняет
    timestamp, service, session_id и interaction_id, упаковывая все переданные
    ключи-значения в поле data.

    Пример использования:
        tlog = make_tech_logger("gw-chat", sid, iid)
        tlog("INFO", headers=headers, text=text)
    """
    def tlog(level: str, **data):
        entry = TechLogEntry(
            timestamp=datetime.now(),
            level=level,
            service=service,
            session_id=session_id,
            interaction_id=interaction_id,
            data=data
        )
        log_tech(entry)
    return tlog
