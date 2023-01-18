from django.urls import path

from api.views import (
    ChannelExistsView,
    ChannelListView,
    ChannelRateView,
    ChannelUnsubscribeView,
    HealthCheckView,
    LoginView,
    MessagesView,
    RegisterView,
    UserView,
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('me', UserView.as_view(), name='me'),
    path('channels', ChannelListView.as_view(), name='channels'),
    path('channels/rates', ChannelRateView.as_view(), name='channels-rates'),
    path('channels/<str:channel>', ChannelUnsubscribeView.as_view(), name='single-channel'),
    path('healthcheck', HealthCheckView.as_view(), name='healthcheck'),
    path('messages', MessagesView.as_view(), name='messages'),
    path('channels/exists/<str:channel>', ChannelExistsView.as_view(), name='channel-exists'),
]
