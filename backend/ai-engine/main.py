import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.agent import tools, llm  # наши инструменты и LLM
from langchain.agents import initialize_agent, AgentType
from models.utils.logging_service import make_human_logger, make_tech_logger

# лемматизатор для логирования
from utils.house_config import _lemmatize

# колбэки для human-log
from langchain.callbacks.base import BaseCallbackHandler

class HumanLoggerCallbackHandler(BaseCallbackHandler):
    def __init__(self, hlog):
        self.hlog = hlog

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.hlog(f"LLM prompt:\n{prompts[0]}", "agent")

    def on_agent_action(self, action, **kwargs):
        self.hlog(f"Agent calls tool `{action.tool}` with input `{action.tool_input}`", "agent")

    def on_tool_end(self, output, **kwargs):
        self.hlog(f"Tool returned: `{output}`", "agent")

    def on_agent_finish(self, finish, **kwargs):
        result = finish.return_values.get("output")
        self.hlog(f"Agent final answer: `{result}`", "agent")

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

app = FastAPI(title="ai-engine")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# инициализируем LangChain-агента раз
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
)

@app.post("/agent/process")
async def process_agent_input(body: AgentInput, request: Request):
    hlog = make_human_logger("ai-engine", body.session_id, body.interaction_id)
    tlog = make_tech_logger("ai-engine", body.session_id, body.interaction_id)

    # 1) исходный запрос
    hlog(f"Получен запрос «{body.input_data}»", "gw-hub")
    # 2) лемматизация
    lemmas = _lemmatize(body.input_data)
    hlog(f"Лемматизация запроса: {lemmas}", "agent")
    # 3) технический лог
    tlog("INFO", input_type=body.input_type, device_id=body.device_id, user_id=body.user_id)

    # колбэк для human-log
    human_cb = HumanLoggerCallbackHandler(hlog)

    # запускаем агента в thread-pool, передавая callbacks
    loop = asyncio.get_running_loop()
    response_text = await loop.run_in_executor(
        None,
        lambda: agent.run(body.input_data, callbacks=[human_cb])
    )

    hlog(f"Отправлен ответ: «{response_text}»", "gw-hub")
    return JSONResponse(
        content=AgentOutput(
            response=response_text,
            session_id=body.session_id,
            interaction_id=body.interaction_id
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 6000)),
        log_level="info",
    )
