FROM python:3.9-slim

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем requirements
COPY requirements.txt .

RUN mkdir temp && mkdir results

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь Wav2Lip-проект
COPY Wav2Lip/ /app/wav2lip/
COPY main.py .
COPY static/ /app/static/


ENV PYTHONPATH=/app/wav2lip

CMD ["python", "main.py"]
