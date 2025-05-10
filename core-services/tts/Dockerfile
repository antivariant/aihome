FROM python:3.11-slim-bookworm

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    libstdc++6 \
    libgomp1 \
    libatomic1 \
    libasound2 \
    sox \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Piper
RUN wget -O /tmp/piper.tar.gz https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_aarch64.tar.gz && \
    mkdir -p /app/piper && \
    tar -xzf /tmp/piper.tar.gz -C /app/piper --strip-components=1 && \
    chmod +x /app/piper/piper && \
    ldconfig /app/piper && \
    rm /tmp/piper.tar.gz

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /shared-wav && chmod 777 /shared-wav

CMD ["python", "main.py"]