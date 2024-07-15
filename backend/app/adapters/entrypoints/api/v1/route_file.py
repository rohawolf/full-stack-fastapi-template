import json

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, status
from fastapi.encoders import jsonable_encoder

from app.adapters.entrypoints import STATUS_CODES
from app.adapters.entrypoints.api.utils import save_file_to_static
from app.core.containers import Container
from app.domain.entities.file import available_file_categories_and_extensions
from app.domain.ports.use_cases.file import FileServiceInterface
from app.domain.schemas.file import FileCreateInput

router = APIRouter()


@router.post("/")
@inject
def upload_file(
    category: str,
    file: UploadFile,
    file_service: FileServiceInterface = Depends(Provide[Container.file_service]),
) -> Response:
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )
    if category not in available_file_categories_and_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category",
        )
    file_name = str(file.filename)
    if (
        file_name.split(".")[-1]
        not in available_file_categories_and_extensions[category]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid extension",
        )

    url = save_file_to_static(file=file, category=category)

    response = file_service.create(
        FileCreateInput(category=category, name=file_name, url=url)
    )
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.get("/{uuid}")
@inject
def get_file(
    uuid: str,
    file_service: FileServiceInterface = Depends(Provide[Container.file_service]),
) -> Response:
    response = file_service.retrieve_file(uuid)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.delete("/{uuid}")
@inject
def delete_file(
    uuid: str,
    file_service: FileServiceInterface = Depends(Provide[Container.file_service]),
) -> Response:
    response = file_service.delete_file_by_id(uuid)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )
