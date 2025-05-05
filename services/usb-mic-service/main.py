import time
import requests
import os

AUDIO_FILE_PATH = "mock_audio.wav"
AUDIO_GATEWAY_URL = os.getenv("AUDIO_GATEWAY_URL", "http://audio-stream-gateway:5050/receive-audio")

print("USB Mic Simulator started", flush=True)

while True:
    try:
        with open(AUDIO_FILE_PATH, "rb") as f:
            files = {'file': ("mock_audio.wav", f, "audio/wav")}
            response = requests.post(AUDIO_GATEWAY_URL, files=files)
            print("Uploaded:", response.status_code, response.text, flush=True)
    except Exception as e:
        print("Error sending audio:", e, flush=True)

    time.sleep(10)
