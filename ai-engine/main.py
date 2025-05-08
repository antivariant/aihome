from fastapi import FastAPI, Request
from pydantic import BaseModel
import redis.asyncio as redis
import os, uvicorn

app = FastAPI()

# Redis connection (если используется)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/")
def read_root():
    return {"status": "langchain-agent up"}

# Входная модель
class AgentInput(BaseModel):
    device_id: str
    user_id: str
    input_type: str
    input: str

@app.post("/agent/process")
async def process_agent_input(payload: AgentInput):
    # TODO: Реализовать цепочку обработки
    return {
        "status": "received",
        "device_id": payload.device_id,
        "user_id": payload.user_id,
        "input_type": payload.input_type
    }



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 6000)))