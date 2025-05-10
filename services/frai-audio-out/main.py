from fastapi import FastAPI, Request
import uvicorn
import os
import requests
from collections import deque

app = FastAPI()

TTS_URL = os.getenv("TTS_URL", "http://svc-tts:5240/speak")
WAV_PATH = os.getenv("TTS_WAV_PATH", "/shared-wav")
HISTORY = {}

@app.post("/speak")
async def speak(req: Request):
    body = await req.json()
    text = body.get("text")
    device_id = body.get("device_id", "default")
    lang = body.get("language", "ru")
    voice = body.get("voice", "irina")
    quality = body.get("quality", "medium")

    if not text:
        return {"error": "text required"}

    # отправляем текст в tts
    resp = requests.post(TTS_URL, json={
        "text": text,
        "language": lang,
        "voice": voice,
        "quality": quality
    })
    if resp.status_code != 200:
        return {"error": "tts error", "details": resp.text}

    data = resp.json()
    filename = os.path.basename(data.get("wav_path"))  # или data["filename"]
    if not filename:
        return {"error": "no wav returned"}

    if device_id not in HISTORY:
        HISTORY[device_id] = deque(maxlen=3)
    HISTORY[device_id].append(filename)

    return {"status": "queued", "filename": filename}

@app.get("/last/{device_id}")
def last(device_id: str):
    if device_id not in HISTORY or not HISTORY[device_id]:
        return {"error": "no history"}
    return {"last": HISTORY[device_id][-1]}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5140)))
