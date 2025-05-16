# gateways/gw-chat/main.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
from pymongo import MongoClient
from datetime import datetime
import os, shutil, uuid, httpx, uvicorn, time

from models.contracts.chat.agent_input import AgentInput
from models.contracts.log.human_log_entry import HumanLogEntry
from models.contracts.log.tech_log_entry import TechLogEntry
from models.utils.logging_service import log_human, log_tech

API_TOKEN = os.getenv("CHAT_API_TOKEN")
GW_HUB_URL = os.getenv("GW_HUB_URL")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
UPLOAD_FOLDER = "/app/uploads"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_client = MongoClient(MONGODB_URI)
db = mongo_client["frai"]
uploads_col = db["chat_uploads"]
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/send")
async def send_input(
    request: Request,
    device_id: str = Form(...),
    user_id: str = Form(...),
    text: str = Form(None),
    file: UploadFile = File(None)
):
    session_id = str(uuid.uuid4())
    interaction_id = str(uuid.uuid4())

    auth = request.headers.get("Authorization")
    if not auth or auth.replace("Bearer ", "") != API_TOKEN:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if (text is None or text.strip() == "") and not file:
        raise HTTPException(status_code=422, detail="Either 'text' or 'file' must be provided.")

    input_type = "text"
    filename = None

    if file:
        ext = os.path.splitext(file.filename)[1]
        file_uuid = uuid.uuid4().hex
        filename = f"{file_uuid}{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        content_type = file.content_type.lower()
        input_type = {
            True: "image",
            content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "excel",
            content_type == "text/markdown": "markdown"
        }.get(content_type.startswith("image/"), "file")

        uploads_col.insert_one({
            "_id": file_uuid,
            "original_name": file.filename,
            "stored_path": f"uploads/{filename}",
            "content_type": content_type,
            "device_id": device_id,
            "user_id": user_id,
            "timestamp": int(time.time()),
            "input_type": input_type,
            "description": "Загружено пользователем через чат"
        })

    log_human(HumanLogEntry(
        timestamp=datetime.now(),
        actor="gw-chat",
        target="gw-hub",
        message=f"Пользователь {user_id} задал вопрос '{text}' с устройства {device_id}",
        session_id=session_id,
        interaction_id=interaction_id
    ))

    log_tech(TechLogEntry(
        timestamp=datetime.now(),
        level="INFO",
        service="gw-chat",
        session_id=session_id,
        interaction_id=interaction_id,
        data={"headers": dict(request.headers), "device_id": device_id, "user_id": user_id, "text": text}
    ))

    agent_input = AgentInput(
        device_id=device_id,
        user_id=user_id,
        input_type=input_type,
        input_data=f"uploads/{filename}" if file else text.strip(),
        session_id=session_id,
        interaction_id=interaction_id
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{GW_HUB_URL}/process", json=agent_input.dict())
        return JSONResponse(content={
            **response.json(),
            "session_id": session_id,
            "interaction_id": interaction_id
        })

@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5121)))
