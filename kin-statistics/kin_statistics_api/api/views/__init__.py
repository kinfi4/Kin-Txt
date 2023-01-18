from api import tasks, views
from config import settings
from config.containers import Container

from .healthcheck import HealthCheckView
from .register_user import RegisterUserView
from .report_data import GetReportDataView
from .reports import ReportsListView, ReportsSingleView

container = Container()
container.config.from_dict(settings.__dict__)
container.init_resources()
container.wire(
    packages=[views],
    modules=[tasks],
)
