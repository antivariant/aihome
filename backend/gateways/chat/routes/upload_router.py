from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from config import UPLOAD_DIR

router = APIRouter()

@router.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, filename=filename)
