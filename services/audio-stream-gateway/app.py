from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import aiofiles, os, uuid
import httpx

app = FastAPI()
UPLOAD_FOLDER = "./recordings"
STT_URL = os.getenv("STT_URL", "http://stt-service:5060/stt")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/receive-audio")
async def receive_audio(request: Request):
    audio_id = uuid.uuid4().hex
    filepath = os.path.join(UPLOAD_FOLDER, f"{audio_id}.wav")

    async with aiofiles.open(filepath, 'wb') as f:
        async for chunk in request.stream():
            await f.write(chunk)

    async with httpx.AsyncClient() as client:
        try:
            with open(filepath, "rb") as f:
                files = {'file': (f"{audio_id}.wav", f, 'audio/wav')}
                response = await client.post(STT_URL, files=files)

            os.remove(filepath)
            return JSONResponse(content=response.json(), status_code=response.status_code)

        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return JSONResponse(content={"error": str(e)}, status_code=500)
