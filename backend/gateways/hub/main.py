# gateways/gw-hub/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, httpx, uvicorn
from datetime import datetime

from models.contracts.chat.agent_input import AgentInput
from models.utils.logging_service import log_human, log_tech
from models.contracts.log.human_log_entry import HumanLogEntry
from models.contracts.log.tech_log_entry import TechLogEntry

from routers import health_routes, log_routes, profile_routes

from fastapi.staticfiles import StaticFiles


AI_ENGINE_URL = os.getenv("AI_ENGINE_URL")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/avatars", StaticFiles(directory="/app/avatars"), name="avatars")

app.include_router(health_routes.router)
app.include_router(log_routes.router)
app.include_router(profile_routes.router)


@app.post("/process")
async def process_agent_input(request: Request):
    body = await request.json()
    session_id = body.get("session_id", "")
    interaction_id = body.get("interaction_id", "")

    log_human(HumanLogEntry(
        timestamp=datetime.now(),
        actor="gw-hub",
        target="ai-engine",
        message=f"Запрос от пользователя {body.get('user_id')} отправлен в AI Engine",
        session_id=session_id,
        interaction_id=interaction_id
    ))

    log_tech(TechLogEntry(
        timestamp=datetime.now(),
        level="INFO",
        service="gw-hub",
        session_id=session_id,
        interaction_id=interaction_id,
        data=body
    ))

    async with httpx.AsyncClient() as client:
        agent_response = await client.post(f"{AI_ENGINE_URL}/agent/process", json=body)

    result = agent_response.json()

    log_human(HumanLogEntry(
        timestamp=datetime.now(),
        actor="ai-engine",
        target="gw-hub",
        message=result.get("response", "Нет ответа"),
        session_id=session_id,
        interaction_id=interaction_id
    ))

    log_tech(TechLogEntry(
        timestamp=datetime.now(),
        level="INFO",
        service="gw-hub",
        session_id=session_id,
        interaction_id=interaction_id,
        data=result
    ))

    return JSONResponse(content=result)

@app.get("/")
def root():
    return {"status": "gw-hub running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5105)))
