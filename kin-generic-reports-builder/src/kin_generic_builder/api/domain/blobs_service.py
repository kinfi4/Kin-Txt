import os
import shutil
import logging
from enum import Enum

from kin_generic_builder.api.entities import User

__all__ = ["BlobsService", "BlobType"]


class BlobType(str, Enum):
    MODEL = "model"
    TOKENIZER = "tokenizer"


class BlobsService:
    def __init__(self, model_storage_path: str) -> None:
        self._storage_path = model_storage_path
        self._logger = logging.getLogger(__name__)

    async def upload_model_binaries(self, user: User, chunk: bytes, model_code: str, chunk_index: int, blob_type: BlobType) -> None:
        user_folder = os.path.join(self._storage_path, user.username)
        if not os.path.exists(user_folder):
            os.mkdir(user_folder)

        model_folder = os.path.join(user_folder, model_code)
        if not os.path.exists(model_folder):
            os.mkdir(model_folder)

        chunk_path = os.path.join(model_folder, f"{blob_type.value}_chunk_{chunk_index}")
        with open(chunk_path, "wb") as f:
            f.write(chunk)

        self._logger.info(f"Chunk {chunk_index} of {blob_type.value} with code {model_code} uploaded successfully")

    async def merge_binaries(self, user: User, model_code: str, total_chunks: int, blob_type: BlobType) -> None:
        model_folder = os.path.join(self._storage_path, user.username, model_code)
        merged_file_path = os.path.join(model_folder, blob_type)

        with open(merged_file_path, "wb") as merged_file:
            for chunk_index in range(total_chunks):
                chunk_path = os.path.join(model_folder, f"{blob_type.value}_chunk_{chunk_index}")
                with open(chunk_path, "rb") as chunk_file:
                    merged_file.write(chunk_file.read())

                os.remove(chunk_path)

        self._logger.info(f"All chunks of {blob_type} for {model_code} merged successfully")

    async def delete_model_binaries(self, user: User, model_code: str) -> None:
        model_folder = os.path.join(self._storage_path, user.username, model_code)
        if os.path.exists(model_folder):
            shutil.rmtree(model_folder)
            self._logger.info(f"Model binaries for {model_code} deleted successfully")
        else:
            self._logger.info(f"Model binaries for {model_code} not found")
