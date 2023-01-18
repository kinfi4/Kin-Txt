from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    def get(self, request: Request) -> Response:
        return Response(data={'status': 'OK'})
