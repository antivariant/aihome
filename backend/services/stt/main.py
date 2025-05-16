from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os, uvicorn
from stt_handler import mock_transcribe

app = FastAPI()

@app.post("/stt")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        transcript = await mock_transcribe(contents)
        return {"transcription": transcript}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5060)))