import logging

from fastapi import APIRouter, UploadFile, File, Form, Depends, status
from fastapi.responses import JSONResponse, Response

from kin_generic_builder.api.domain import BlobsService, BlobType
from kin_generic_builder.api.domain.blobs_service import FileIntegrityError
from kin_generic_builder.settings import Settings
from kin_generic_builder.api.entities import User
from kin_generic_builder.api.views.helpers import get_current_user

router = APIRouter(prefix="/blobs")

_logger = logging.getLogger(__name__)


@router.post("/upload")
async def upload_model_binaries(
    current_user: User = Depends(get_current_user),
    chunk: UploadFile = File(...),
    model_code: str = Form(...),
    chunk_index: int = Form(...),
    total_chunks: int = Form(...),
    blob_type: BlobType = Form(...),
    chuck_hash: str = Form(...),
):
    service = BlobsService(Settings().model_storage_path)

    try:
        await service.upload_model_binaries(
            user=current_user,
            chunk=await chunk.read(),
            model_code=model_code,
            chunk_index=chunk_index,
            blob_type=blob_type,
            chuck_hash=chuck_hash,
        )
    except FileIntegrityError as e:
        _logger.error(f"Incorrect file hash: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": "Incorrect file hash, it seems like file was corrupted during the upload"},
        )
    except Exception as e:
        _logger.error(f"Error while uploading the chunk: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"errors": "Something went wrong while uploading the chunk"},
        )

    if chunk_index == total_chunks - 1:
        try:
            await service.merge_binaries(
                user=current_user,
                model_code=model_code,
                blob_type=blob_type,
                total_chunks=total_chunks
            )
        except Exception as e:
            _logger.error(f"Error while merging the chunks for mode with code {model_code}: {e}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"errors": "Something went wrong while merging the chunk"},
            )

        return JSONResponse(content={"message": "All binaries uploaded and merged successfully"})

    return JSONResponse(content={"message": "Chunk uploaded successfully"})


@router.delete("/delete/{model_code}")
async def delete_model_binaries(
    model_code: str,
    current_user: User = Depends(get_current_user),
):
    service = BlobsService(Settings().model_storage_path)

    try:
        await service.delete_model_binaries(
            user=current_user,
            model_code=model_code,
        )
    except Exception as e:
        _logger.error(f"Error while deleting the model binaries: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"errors": "Something went wrong while deleting the model binaries"},
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
