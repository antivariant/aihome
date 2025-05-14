from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED
from pymongo import MongoClient
from datetime import datetime
import os, shutil, uuid, httpx, uvicorn, time, logging

# === ENV ===
API_TOKEN = os.getenv("CHAT_API_TOKEN")
AGENT_URL = os.getenv("AGENT_URL")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
UPLOAD_FOLDER = "./uploads"
LOG_FOLDER = "./logs"

# === FastAPI ===
app = FastAPI()

# === MongoDB ===
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client["frai"]
uploads_col = db["chat_uploads"]

# === Loggers ===
os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

tech_logger = logging.getLogger("tech")
human_logger = logging.getLogger("human")
tech_handler = logging.FileHandler(f"{LOG_FOLDER}/tech.log")
human_handler = logging.FileHandler(f"{LOG_FOLDER}/human.log")
tech_logger.addHandler(tech_handler)
human_logger.addHandler(human_handler)
tech_logger.setLevel(logging.INFO)
human_logger.setLevel(logging.INFO)

def log_event(device_id, user_id, filename, input_type):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tech_logger.info(f"[{now}] Received file '{filename}' ({input_type}) from {device_id} user={user_id}")
    human_logger.info(f"[{now}] Пользователь {user_id} загрузил файл '{filename}', Frai передал его AI-агенту.")

# === Routes ===
@app.post("/send")
async def send_input(
    request: Request,
    device_id: str = Form(...),
    user_id: str = Form(...),
    input: str = Form(None),
    file: UploadFile = File(None)
):
    # Auth check
    auth = request.headers.get("Authorization")
    if not auth or auth.replace("Bearer ", "") != API_TOKEN:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")

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
        if content_type.startswith("image/"):
            input_type = "image"
        elif content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            input_type = "excel"
        elif content_type == "text/markdown":
            input_type = "markdown"
        else:
            input_type = "file"

        # Save metadata in DB
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

        log_event(device_id, user_id, file.filename, input_type)

    payload = {
        "device_id": device_id,
        "user_id": user_id,
        "input_type": input_type,
        "input_data": f"uploads/{filename}" if file else input
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(AGENT_URL, json=payload)
        return JSONResponse(content=response.json())

@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    tech_logger.info(f"GET /uploads/{filename} served")
    return FileResponse(path=file_path, filename=filename)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5121)))
