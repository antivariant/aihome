from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import subprocess
import uuid
import logging

app = FastAPI()

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = os.getenv("WAV_OUTPUT_DIR", "/shared-wav")
BASE_MODEL_DIR = os.getenv("MODELS_DIR", "/models")
PIPER_PATH = "/app/piper/piper"  # Теперь правильный путь

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BASE_MODEL_DIR, exist_ok=True)

def run_piper(command):
    """Запускает piper с правильными переменными окружения"""
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app/piper:" + env.get("LD_LIBRARY_PATH", "")
    
    try:
        result = subprocess.run(
            command,
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Piper failed: {e.stderr}")
        raise

@app.post("/speak")
async def speak(request: Request):
    try:
        body = await request.json()
        text = body.get("text")
        if not text:
            raise HTTPException(status_code=400, detail="Text not provided")

        model_path = "/models/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx"
        config_path = "/models/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json"
        
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model not found")
        
        uid = str(uuid.uuid4())
        raw_path = f"/shared-wav/{uid}.raw"
        wav_path = f"/shared-wav/{uid}.wav"

        # Запускаем Piper с выводом в raw файл
        cmd = [
            "/app/piper/piper",
            "--model", model_path,
            "--config", config_path,
            "--output_file", raw_path
        ]
        
        # Передаем текст через stdin
        result = subprocess.run(
            cmd,
            input=text,
            text=True,
            capture_output=True
        )
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Piper failed: {result.stderr}"
            )

        # Конвертируем raw в wav с помощью sox
        subprocess.run([
            "sox",
            "-r", "22050",
            "-e", "signed-integer",
            "-b", "16",
            "-c", "1",
            raw_path,
            wav_path
        ], check=True)
        
        os.remove(raw_path)  # Удаляем временный raw файл
        
        return {"wav_path": wav_path}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5240")),
        workers=1
    )