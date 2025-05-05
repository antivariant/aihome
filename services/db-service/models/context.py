from pydantic import BaseModel
from typing import Optional

class ContextModel(BaseModel):
    user_id: str
    session_id: str
    message: str
    timestamp: Optional[str]
