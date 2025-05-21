# gateways/gw-hub/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn, os

import init
from routers.health_routes    import router as health_router
from routers.log_routes       import router as log_router
from routers.profile_routes   import router as profile_router
from routers.process_question_router import router as send_engine_router

# Создание FastAPI-приложения
app = FastAPI(title="gw-hub")

# Настройка CORS из config
app.add_middleware(
    CORSMiddleware,
    allow_origins=init.ALLOWED_ORIGINS,
    allow_credentials=init.ALLOW_CREDENTIALS,
    allow_methods=init.ALLOWED_METHODS,
    allow_headers=init.ALLOWED_HEADERS,
)

# Статика аватаров
app.mount(
    "/avatars",
    StaticFiles(directory=init.AVATARS_DIR),
    name="avatars"
)

# Регистрация роутеров
app.include_router(health_router,      prefix="", tags=["health"])
app.include_router(log_router,         prefix="", tags=["logs"])
app.include_router(profile_router,     prefix="", tags=["profiles"])
app.include_router(send_engine_router, prefix="", tags=["engine"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", init.PORT))
    )
