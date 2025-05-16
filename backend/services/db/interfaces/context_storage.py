from clients.mongo_client import db
from models.context import ContextModel

def save_context(data: dict):
    context = ContextModel(**data)
    result = db.contexts.insert_one(context.dict())
    return {"inserted_id": str(result.inserted_id)}
