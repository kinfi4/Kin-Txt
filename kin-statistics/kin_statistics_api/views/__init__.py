from fastapi import APIRouter

from kin_statistics_api.constants import API_ROUTE_PATH
from kin_statistics_api.views.reports import router as reports_router
from kin_statistics_api.views.report_data import router as reports_data_router


api_router = APIRouter(prefix=API_ROUTE_PATH)

api_router.include_router(reports_router)
api_router.include_router(reports_data_router)
