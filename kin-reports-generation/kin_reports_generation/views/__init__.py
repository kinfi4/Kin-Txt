from fastapi import APIRouter

from .model import router as model_router
from .visualization_template import router as visualization_template_router

api_router = APIRouter()

api_router.include_router(model_router)
api_router.include_router(visualization_template_router)
