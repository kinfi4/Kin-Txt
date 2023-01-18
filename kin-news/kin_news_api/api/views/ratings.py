from dependency_injector.wiring import Provide, inject
from pydantic import ValidationError
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.domain.entities import RatePostEntity
from api.domain.services import RatingsService
from api.exceptions import ChannelDoesNotExists
from config.containers import Container
from kin_news_core.auth import JWTAuthentication
from kin_news_core.utils import pydantic_errors_prettifier


class ChannelRateView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated,)

    @inject
    def get(
        self,
        request: Request,
        rating_service: RatingsService = Provide[Container.domain_services.rating_service],
    ) -> Response:
        channel_link = request.query_params.get('channel')

        if not channel_link:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'errors': 'Please provide a channel name'}
            )

        ratings = rating_service.get_channel_rating_stats(request.user, channel_link)

        return Response(data=ratings.dict(by_alias=True))

    @inject
    def post(
        self,
        request: Request,
        rating_service: RatingsService = Provide[Container.domain_services.rating_service],
    ) -> Response:
        try:
            channel_rate_entity = RatePostEntity(**request.data)
            ratings = rating_service.rate_channel(request.user, channel_rate_entity)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': pydantic_errors_prettifier(err.errors())})
        except ChannelDoesNotExists as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})

        return Response(data=ratings.dict(by_alias=True))
