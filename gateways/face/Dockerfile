FROM python:3.8-slim-bookworm

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    build-essential \
    cmake \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# SadTalker code
COPY SadTalker/ /app/sadtalker/
COPY requirements.txt .
COPY main.py .

# Установка зависимостей
RUN pip install --no-cache-dir pip==23.2.1 && \
    pip install -r requirements.txt && \
    pip install dlib

ENV PYTHONPATH=/app/sadtalker

CMD ["python", "main.py"]
