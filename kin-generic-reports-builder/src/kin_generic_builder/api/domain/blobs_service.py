import os
import shutil
import logging
import hashlib
from enum import Enum

from fastapi import UploadFile

from kin_generic_builder.api.entities import User
from kin_generic_builder.mixins import UnpackKerasArchiveMixin

__all__ = ["BlobsService", "BlobType", "FileIntegrityError", "FileValidationError"]


class BlobType(str, Enum):
    MODEL = "model"
    TOKENIZER = "tokenizer"
    STOP_WORDS = "stop_words"


class FileIntegrityError(Exception):
    pass


class FileValidationError(Exception):
    pass


class BlobsService(UnpackKerasArchiveMixin):
    _ALLOWED_STOP_WORDS_EXTENSIONS = ["csv", "txt", "json"]

    def __init__(self, model_storage_path: str) -> None:
        self._storage_path = model_storage_path
        self._logger = logging.getLogger(__name__)

    async def upload_model_binaries(
        self,
        user: User,
        chunk: UploadFile,
        model_code: str,
        chunk_index: int,
        blob_type: BlobType,
        chuck_hash: str,
    ) -> None:
        await self._validate_chunk_file(chunk, blob_type)
        chunk = await chunk.read()

        user_folder = os.path.join(self._storage_path, user.username)
        if not os.path.exists(user_folder):
            os.mkdir(user_folder)

        model_folder = os.path.join(user_folder, model_code)
        if not os.path.exists(model_folder):
            os.mkdir(model_folder)

        chunk_path = os.path.join(model_folder, f"{blob_type.value}_chunk_{chunk_index}")
        with open(chunk_path, "wb") as f:
            f.write(chunk)

        await self._verify_file_hash(chunk_path, chuck_hash)

        self._logger.info(f"Chunk {chunk_index} of {blob_type.value} with code {model_code} uploaded successfully")

    async def merge_binaries(self, user: User, model_code: str, total_chunks: int, blob_type: BlobType) -> None:
        model_folder = os.path.join(self._storage_path, user.username, model_code)
        merged_file_path = os.path.join(model_folder, blob_type)

        if os.path.exists(merged_file_path) and os.path.isdir(merged_file_path):
            shutil.rmtree(merged_file_path)

        with open(merged_file_path, "wb") as merged_file:
            for chunk_index in range(total_chunks):
                chunk_path = os.path.join(model_folder, f"{blob_type.value}_chunk_{chunk_index}")
                with open(chunk_path, "rb") as chunk_file:
                    merged_file.write(chunk_file.read())

                os.remove(chunk_path)

        self._logger.info(f"All chunks of {blob_type} for {model_code} merged successfully")

        self._unpack_archive_if_needed(merged_file_path)

    async def delete_model_binaries(self, user: User, model_code: str) -> None:
        model_folder = os.path.join(self._storage_path, user.username, model_code)
        if os.path.exists(model_folder):
            shutil.rmtree(model_folder)
            self._logger.info(f"Model binaries for {model_code} deleted successfully")
        else:
            self._logger.info(f"Model binaries for {model_code} not found")

    async def _verify_file_hash(self, file_path: str, expected_hash: str) -> None:
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        if file_hash != expected_hash:
            raise FileIntegrityError(f"File {file_path} has incorrect hash")

    async def _validate_chunk_file(self, chunk: UploadFile, blob_type: BlobType) -> None:
        if blob_type == BlobType.STOP_WORDS and chunk.filename.split(".")[-1] not in self._ALLOWED_STOP_WORDS_EXTENSIONS:
            raise FileValidationError(f"File {chunk.filename} has incorrect extension for stop-words file, expected .txt, .csv or .json")
