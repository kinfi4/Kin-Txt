from api import views
from config import settings
from config.containers import Container

from .channels import ChannelExistsView, ChannelListView, ChannelUnsubscribeView
from .healthcheck import HealthCheckView
from .messages import MessagesView
from .ratings import ChannelRateView
from .user import LoginView, RegisterView, UserView

container = Container()
container.config.from_dict(settings.__dict__)
container.init_resources()
container.wire(packages=[views])
