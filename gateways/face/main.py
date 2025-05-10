from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os, uuid, subprocess, uvicorn

app = FastAPI()

DEFAULT_VIDEO = "static/loop_base.mp4"
DEFAULT_AUDIO = "static/sample.wav"
CHECKPOINT = "wav2lip/checkpoints/wav2lip.pth"
RESULT_PATH = "results/result_voice.mp4"

@app.post("/generate")
async def generate(
    audio: UploadFile = File(None),
    video: UploadFile = File(None),
    pads: str = Form("0 10 0 0"),
    resize_factor: str = Form("1"),
    nosmooth: bool = Form(True)
):
    session_id = str(uuid.uuid4())
    session_dir = f"output/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    if os.path.exists(RESULT_PATH):
        os.remove(RESULT_PATH)

    print(f"[INFO] Session: {session_id}")

    # Видео
    if video:
        video_path = f"{session_dir}/video.mp4"
        with open(video_path, "wb") as f:
            f.write(await video.read())
    else:
        video_path = DEFAULT_VIDEO
    print(f"[INFO] Video path: {video_path}")

    # Аудио
    if audio:
        audio_path = f"{session_dir}/audio.wav"
        with open(audio_path, "wb") as f:
            f.write(await audio.read())
    else:
        audio_path = DEFAULT_AUDIO
    print(f"[INFO] Audio path: {audio_path}")

    if not os.path.exists(video_path) or not os.path.exists(audio_path):
        raise HTTPException(status_code=400, detail="Video or audio not found")

    # Запуск Wav2Lip
    cmd = [
        "python", "wav2lip/inference.py",
        "--checkpoint_path", CHECKPOINT,
        "--face", video_path,
        "--audio", audio_path,
        "--pads", *pads.strip().split(),
        "--resize_factor", resize_factor
    ]
    if nosmooth:
        cmd.append("--nosmooth")

    print(f"[INFO] Running Wav2Lip with: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0 or not os.path.exists(RESULT_PATH):
        print(f"[ERROR] Wav2Lip failed.")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Wav2Lip inference failed",
                "stdout": result.stdout[-500:],
                "stderr": result.stderr[-500:]
            }
        )

    # Переименовываем файл для возврата
    final_path = f"{session_dir}/final.mp4"
    os.rename(RESULT_PATH, final_path)
    print(f"[SUCCESS] Generated: {final_path}")

    return FileResponse(final_path, media_type="video/mp4")


@app.get("/")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5180)))
