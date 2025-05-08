from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os, uuid, subprocess, uvicorn

app = FastAPI()


@app.post("/generate")
async def generate(audio: UploadFile = File(...), image: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    session_dir = f"output/{session_id}"
    os.makedirs(session_dir, exist_ok=True)

    audio_path = f"{session_dir}/audio.wav"
    image_path = f"{session_dir}/avatar.jpg"
    video_path = f"{session_dir}/video.mp4"
    resized_path = f"{session_dir}/resized.mp4"
    log_path = f"{session_dir}/inference.log"

    with open(audio_path, "wb") as f:
        f.write(await audio.read())
    with open(image_path, "wb") as f:
        f.write(await image.read())

    if os.path.getsize(audio_path) < 1024 or os.path.getsize(image_path) < 1024:
        raise HTTPException(status_code=400, detail="Audio or image file too small")

    cmd = [
        "python", "sadtalker/inference.py",
        "--driven_audio", audio_path,
        "--source_image", image_path,
        "--result_dir", session_dir,
        "--still",
        "--size", "256",
        "--no-enhancer"
    ]

    print("Running SadTalker with:", " ".join(cmd))

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    with open(log_path, "w") as log_file:
        log_file.write("=== STDOUT ===\n")
        log_file.write(result.stdout)
        log_file.write("\n=== STDERR ===\n")
        log_file.write(result.stderr)

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"inference.py failed. See logs in {log_path}")

    generated = next((f for f in os.listdir(session_dir) if f.endswith(".mp4") and not f.startswith("resized")), None)
    if not generated:
        raise HTTPException(status_code=500, detail=f"No .mp4 output. Check logs: {log_path}")
    os.rename(f"{session_dir}/{generated}", video_path)

    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path,
            "-vf", "scale=128:150", resized_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"ffmpeg failed: {e}")

    if os.path.getsize(resized_path) < 10000:
        raise HTTPException(status_code=500, detail="Resized video is too small")

    return FileResponse(resized_path, media_type="video/mp4")

@app.get("/")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5180)))
