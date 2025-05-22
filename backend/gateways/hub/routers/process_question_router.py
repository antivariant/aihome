# routers/process_question_routes.py

from fastapi import APIRouter, Request, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from httpx import AsyncClient, Timeout

import init as init
from models.contracts.chat.agent_input import AgentInput
from models.utils.logging_service import make_human_logger, make_tech_logger

router = APIRouter()

@router.post("/process/question")
async def send_to_engine(input: AgentInput, request: Request):
    # Логгеры
    hlog = make_human_logger("gw-hub", input.session_id, input.interaction_id)
    tlog = make_tech_logger("gw-hub", input.session_id, input.interaction_id)

    # Логируем отправку в AI Engine
    hlog(
        message=f"Отправка запроса сессии {input.session_id} в AI Engine",
        target="ai-engine"
    )
    tlog(
        level="INFO",
        action="send_to_engine",
        data=input.dict()
    )

    # HTTP-запрос к AI Engine
    async with AsyncClient(timeout=Timeout(60.0, connect=5.0)) as client:
        resp = await client.post(f"{init.AI_ENGINE_URL}/agent/process", json=input.model_dump(), timeout=60.0)

    if resp.status_code != 200:
        tlog(
            level="ERROR",
            action="receive_from_engine",
            error=resp.text
        )
        raise HTTPException(status_code=resp.status_code, detail="Ошибка от AI Engine")

    result = resp.json()

    # Логируем ответ от AI Engine
    hlog(
        message=f"Получен ответ от AI Engine: {result.get('output', '')}",
        target="gw-chat"
    )
    tlog(
        level="INFO",
        action="receive_from_engine",
        data=result
    )

    return result
