import sounddevice as sd
import numpy as np
import requests
import wave
import os
import uuid
import time
from io import BytesIO

DEVICE_ID = os.getenv("DEVICE_ID", "dev-macbook-001")
IS_FRAI = os.getenv("IS_FRAI", "false").lower() == "true"
TARGET_URL = os.getenv("TARGET_URL", "http://svc-audio-in:5231/ingest")
SAMPLE_RATE = 16000
CHUNK_DURATION = float(os.getenv("CHUNK_DURATION", "2.0"))  # in seconds
OVERLAP_DURATION = float(os.getenv("OVERLAP_DURATION", "0.5"))  # in seconds
CHANNELS = 1

BUFFER_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)
OVERLAP_SIZE = int(SAMPLE_RATE * OVERLAP_DURATION)

print("🎙️ Starting MacBook mic driver...", flush=True)

stream_buffer = np.zeros(0, dtype=np.int16)


def send_wav_chunk(data):
    timestamp = int(time.time())
    file_id = f"{DEVICE_ID}-{timestamp}-{uuid.uuid4().hex[:6]}"
    wav_bytes = BytesIO()

    with wave.open(wav_bytes, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.tobytes())

    wav_bytes.seek(0)

    files = {
        "file": (f"{file_id}.wav", wav_bytes, "audio/wav"),
        "metadata": (None, f'''{{
            "device_id": "{DEVICE_ID}",
            "isFrai": {str(IS_FRAI).lower()},
            "timestamp": {timestamp}
        }}''', "application/json")
    }

    try:
        response = requests.post(TARGET_URL, files=files)
        print(f"✅ Sent {file_id}.wav → {response.status_code}", flush=True)
    except Exception as e:
        print(f"❌ Error sending audio chunk: {e}", flush=True)


def audio_callback(indata, frames, time_info, status):
    global stream_buffer
    if status:
        print(f"⚠️ Stream status: {status}", flush=True)

    stream_buffer = np.concatenate((stream_buffer, indata.copy().flatten()))

    while len(stream_buffer) >= BUFFER_SIZE:
        chunk = stream_buffer[:BUFFER_SIZE]
        send_wav_chunk(chunk)
        stream_buffer = stream_buffer[BUFFER_SIZE - OVERLAP_SIZE:]


with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16', callback=audio_callback):
    print("🎧 Listening...")
    while True:
        time.sleep(1)
