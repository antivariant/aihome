from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED
from dotenv import load_dotenv
import os, shutil, uuid, httpx, uvicorn

load_dotenv()
API_TOKEN = os.getenv("CHAT_API_TOKEN")
AGENT_URL = os.getenv("AGENT_URL")
UPLOAD_FOLDER = "./uploads"

app = FastAPI()

class TextPayload(BaseModel):
    device_id: str
    user_id: str
    input: str

def check_token(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or auth.replace("Bearer ", "") != API_TOKEN:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@app.post("/send")
async def send_input(
    request: Request,
    device_id: str = Form(...),
    user_id: str = Form(...),
    input: str = Form(None),
    file: UploadFile = File(None)
):
    check_token(request)

    filename = None
    input_type = "text"

    if file:
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        content_type = file.content_type.lower()
        if content_type.startswith("image/"):
            input_type = "image"
        else:
            input_type = "file"

    payload = {
        "device_id": device_id,
        "user_id": user_id,
        "input_type": input_type,
        "input": filename if file else input
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(AGENT_URL, json=payload)
        return JSONResponse(content=response.json())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5072)))