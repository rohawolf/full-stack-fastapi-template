import json

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.adapters.entrypoints import STATUS_CODES
from app.core.containers import Container
from app.domain.ports.use_cases.user import (
    UserAuthCodeServiceInterface,
    UserServiceInterface,
)
from app.domain.schemas.user import (
    UserAuthCodeCreateInput,
    UserAuthCodeOutput,
    UserAuthCodeUpdateInput,
    UserCreateInput,
    UserUpdateInput,
)

user_router, authentication_router = APIRouter(), APIRouter()


@user_router.post("/")
@inject
def create_user(
    user_create: UserCreateInput,
    user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
) -> Response:
    response = user_service.create(user=user_create)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@user_router.post("/validate-input")
@inject
def validate_user_create_input(
    user_create: UserCreateInput,
    user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
) -> Response:
    response = user_service.validate_user_create_input(user_create)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@user_router.get("/{email}")
@inject
def read_user(
    email: str,
    user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
) -> Response:
    response = user_service.retrieve_user(email)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@user_router.put("/{email}")
@inject
def update_user(
    email: str,
    user_update: UserUpdateInput,
    user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
) -> Response:
    response = user_service.update_user_by_email(email, user_update)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@authentication_router.post("/")
@inject
def create_user_auth_code(
    user_auth_code: UserAuthCodeCreateInput,
    user_auth_code_service: UserAuthCodeServiceInterface = Depends(
        Provide[Container.user_auth_code_service]
    ),
) -> Response:
    response = user_auth_code_service.create(user_auth_code=user_auth_code)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@authentication_router.get("/")
@inject
def read_user_auth_code(
    email: str,
    auth_code: str,
    user_auth_code_service: UserAuthCodeServiceInterface = Depends(
        Provide[Container.user_auth_code_service]
    ),
) -> Response:
    response = user_auth_code_service.retrieve_user_auth_code(email, auth_code)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@authentication_router.put("/")
@inject
def update_user_auth_code(
    email: str,
    auth_code: str,
    user_auth_code: UserAuthCodeUpdateInput,
    user_auth_code_service: UserAuthCodeServiceInterface = Depends(
        Provide[Container.user_auth_code_service]
    ),
) -> Response:
    response = user_auth_code_service.update_user_auth_code_by_email_and_auth_code(
        email, auth_code, user_auth_code
    )
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@authentication_router.get("/validate")
@inject
def validate_user_auth_code(
    email: str,
    auth_code: str,
    user_auth_code_service: UserAuthCodeServiceInterface = Depends(
        Provide[Container.user_auth_code_service]
    ),
) -> UserAuthCodeOutput:
    user_auth_code: UserAuthCodeOutput | None = (
        user_auth_code_service.validate_user_auth_code(email, auth_code)
    )
    if user_auth_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Valid user auth code not found",
        )

    return user_auth_code
