from fastapi import APIRouter

from .upload import router as upload_router

api_router = APIRouter(prefix="/api/generic-builder/v1")

api_router.include_router(upload_router)
