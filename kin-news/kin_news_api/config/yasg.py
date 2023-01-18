from django.urls import path
from drf_yasg.openapi import Contact, Info
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    Info(
        title='Kin New',
        description='Api for Kin News',
        default_version='v1',
        contact=Contact('github/kinfi4')
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-with-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-with-ui'),
]
