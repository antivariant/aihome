FROM python:3.13.3-slim-bookworm

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir fastapi uvicorn pymongo redis pydantic

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8090"]
