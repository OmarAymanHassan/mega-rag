from fastapi import FastAPI, APIRouter,Depends
from utils.config import get_settings,Settings
import os


base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get("/")
async def welcome(app_settings:Settings=Depends(get_settings)):

    #app_settings = get_settings()

    return {

        "APP_NAME": app_settings.APP_NAME,
        "APP_VERSION": app_settings.APP_VERSION
    }


