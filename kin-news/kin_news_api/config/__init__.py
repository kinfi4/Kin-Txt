import logging

from . import settings


logging.basicConfig(
    level=settings.LOG_LEVEL
)
