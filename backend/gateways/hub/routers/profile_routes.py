from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.system_profiles import SYSTEM_PROFILES

router = APIRouter()

@router.get("/profiles")
def get_profiles():
    return JSONResponse(content=SYSTEM_PROFILES)
