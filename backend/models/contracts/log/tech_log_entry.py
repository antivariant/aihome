from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class TechLogEntry(BaseModel):
    timestamp: datetime
    level: str  # INFO, ERROR, DEBUG и т.д.
    service: str  # eg. gw-chat
    session_id: str
    data: Dict[str, Any]  # произвольный payload
