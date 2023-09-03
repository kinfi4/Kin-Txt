import os
import shutil
import logging

from kin_generic_builder.events import ModelDeleted
from kin_generic_builder.settings import Settings

_logger = logging.getLogger(__name__)


def handle_delete_event(event: ModelDeleted) -> None:
    _logger.info(f"Deleting binaries for model: {event.code}")
    model_storage_path = Settings().model_storage_path

    shutil.rmtree(
        os.path.join(model_storage_path, event.username, event.code),
        ignore_errors=True,
    )
