from django.urls import path

from api.views import (
    GetReportDataView,
    HealthCheckView,
    RegisterUserView,
    ReportsListView,
    ReportsSingleView,
)

urlpatterns = [
    path('healthcheck', HealthCheckView.as_view(), name='healthcheck'),
    path('reports', ReportsListView.as_view(), name='reports'),
    path('reports/<int:report_id>', ReportsSingleView.as_view(), name='reports-single'),
    path('users', RegisterUserView.as_view(), name='users'),
    path('data/<int:report_id>', GetReportDataView.as_view(), name='report-data'),
]
