from pydantic import BaseModel

class AgentInput(BaseModel):
    device_id: str
    user_id: str
    input_type: str
    input_data: str
    session_id: str
    interaction_id: str
