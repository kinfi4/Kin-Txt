from fastapi import APIRouter

from .model import router as model_router

api_router = APIRouter()

api_router.include_router(model_router)
