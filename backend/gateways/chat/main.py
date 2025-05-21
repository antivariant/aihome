from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.question_router import router as question_router
from routes.upload_router import router as upload_router
import uvicorn, os

app = FastAPI(title="gw-chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# регистрация роутеров
app.include_router(question_router,   prefix="",      tags=["chat"])
app.include_router(upload_router, prefix="",      tags=["uploads"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 5121)))
