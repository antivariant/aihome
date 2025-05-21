# main.py
import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from agents.agent import handle_user_message
from models.utils.logging_service import make_human_logger
from models.utils.agent_callbacks import AgentMongoLogger

app = FastAPI()

class BodyModel(BaseModel):
    input_data: str
    session_id: str
    interaction_id: str

@app.post("/agent/process")
async def process(body: BodyModel):
    # 1) залогировать вход пользователя
    hlog = make_human_logger(
        actor="gw-chat",
        session_id=body.session_id,
        interaction_id=body.interaction_id,
    )
    hlog(body.input_data, target="ai-engine")

    # 2) подготовить колбэк для логирования Thought/Action/Observation
    agent_logger = AgentMongoLogger(
        session_id=body.session_id,
        interaction_id=body.interaction_id,
        actor="ai-engine",
        target="ai-engine",
    )

    # 3) запустить агента с колбэками
    output = await handle_user_message(
        body.input_data,
        callbacks=[agent_logger],
    )
    return {"output": output}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 6000)),
        log_level="info",
    )
