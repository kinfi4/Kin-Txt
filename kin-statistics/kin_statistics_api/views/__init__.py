from fastapi import APIRouter

from kin_statistics_api.views.reports import router as reports_router
from kin_statistics_api.views.report_data import router as reports_data_router


api_router = APIRouter(prefix='/api/v1')

api_router.include_router(reports_router)
api_router.include_router(reports_data_router)
