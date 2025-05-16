# models/contracts/log/human_log_entry.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HumanLogEntry(BaseModel):
    timestamp: datetime
    actor: str
    target: str
    message: str
    session_id: str
    interaction_id: str  # идентификатор одного запроса-ответа
    profile: Optional[dict] = None
