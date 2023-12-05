from fastapi import APIRouter, Request


router = APIRouter(prefix="/blobs")


@router.get("")
def upload_model_binaries(
    request: Request,
):
    print("GOT REQUEST")
