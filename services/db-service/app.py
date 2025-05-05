from fastapi import FastAPI
from interfaces.context_storage import save_context

app = FastAPI()

@app.get("/")
def root():
    return {"status": "db-service running"}

@app.post("/context/save")
def save(data: dict):
    return save_context(data)
