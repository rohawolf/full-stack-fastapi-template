from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from pydantic_core import ValidationError
from starlette.middleware.cors import CORSMiddleware

from app.adapters.db.orm import start_mappers
from app.adapters.entrypoints.api.base import api_router
from app.core.config import settings
from app.core.containers import Container


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


def start_application() -> FastAPI:
    container = Container()
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        generate_unique_id_function=custom_generate_unique_id,
    )
    if settings.BACKEND_CORS_ORIGINS:
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app_.container = container  # type: ignore
    app_.mount(
        "/static",
        StaticFiles(directory="app/adapters/entrypoints/static"),
        name="static",
    )

    app_.include_router(api_router, prefix=settings.API_V1_STR)
    start_mappers()

    @app_.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request,  # noqa
        exc: ValidationError,
    ) -> JSONResponse:
        # Get the original 'detail' list of errors
        details = exc.errors()
        modified_details = []
        # Replace 'msg' with 'message' for each error
        for error in details:
            modified_details.append(
                {
                    "loc": error["loc"],
                    "message": error["msg"],
                    "type": error["type"],
                }
            )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": modified_details}),
        )

    return app_
