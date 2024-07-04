from fastapi import APIRouter

from app.adapters.entrypoints.api.v1 import (
    route_login,
    route_user,
)

api_router = APIRouter()
api_router.include_router(route_user.user_router, prefix="/users", tags=["users"])
api_router.include_router(
    route_user.authentication_router,
    prefix="/authentications",
    tags=["authentications"],
)
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
