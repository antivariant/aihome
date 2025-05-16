# main.py — ai-engine
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os, uvicorn

from models.contracts.log.human_log_entry import HumanLogEntry
from models.contracts.log.tech_log_entry import TechLogEntry
from models.utils.logging_service import log_human, log_tech

class AgentInput(BaseModel):
    device_id: str
    user_id: str
    input_type: str
    input_data: str
    session_id: str
    interaction_id: str

class AgentOutput(BaseModel):
    response: str
    session_id: str
    interaction_id: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/agent/process")
async def process_agent_input(input: AgentInput, request: Request):
    # Лог: вход от шлюза
    log_human(HumanLogEntry(
        timestamp=datetime.now(),
        actor="ai-engine",
        target="gw-hub",
        message=f"Агент получил запрос от {input.user_id}: '{input.input_data}'",
        session_id=input.session_id,
        interaction_id=input.interaction_id
    ))

    log_tech(TechLogEntry(
        timestamp=datetime.now(),
        level="INFO",
        service="ai-engine",
        session_id=input.session_id,
        interaction_id=input.interaction_id,
        data={
            "input_type": input.input_type,
            "input_data": input.input_data
        }
    ))

    # Имитация ответа
    response_text = f"👋 Привет, {input.input_data}!"

    log_human(HumanLogEntry(
        timestamp=datetime.now(),
        actor="ai-engine",
        target="gw-chat",
        message=f"Агент отвечает: {response_text}",
        session_id=input.session_id,
        interaction_id=input.interaction_id
    ))

    return JSONResponse(content=AgentOutput(
        response=response_text,
        session_id=input.session_id,
        interaction_id=input.interaction_id
    ).dict())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 6000)))
