FROM python:3.13.3-slim-bookworm

WORKDIR /app

# Установка PortAudio и зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libasound2-dev \
    libportaudio2 \
    portaudio19-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
