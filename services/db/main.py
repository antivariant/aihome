import os
from fastapi import FastAPI
from interfaces.context_storage import save_context
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"status": "db-service running"}

@app.post("/context/save")
def save(data: dict):
    return save_context(data)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5063)))