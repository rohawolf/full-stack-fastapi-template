from datetime import timedelta

import jwt
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.adapters.entrypoints.api.utils import OAuth2PasswordBearerWithCookie
from app.core.common.security import create_access_token
from app.core.config import settings
from app.core.containers import Container
from app.domain.ports.use_cases.user import UserServiceInterface
from app.domain.schemas.token import Token
from app.domain.schemas.user import UserLoginInput, UserOutput

router = APIRouter()


@router.post("/token")
@inject
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
) -> Token:
    user_in = UserLoginInput(email=form_data.username, password=form_data.password)
    user: UserOutput | None = user_service.authenticate_user(user_in)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return Token.model_validate({"access_token": access_token, "token_type": "bearer"})


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


@inject
def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
) -> UserOutput:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload: dict[str, str] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM]
        )
        email: str | None = payload.get("sub")
        print("email extracted is ", email)
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError as e:
        raise credentials_exception from e
    with user_service.unit_of_work as tx:
        user = tx.users.get(email)
        if user is None:
            raise credentials_exception

        return UserOutput.model_validate(user)


@inject
def get_current_admin_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserServiceInterface = Depends(Provide[Container.user_service]),
) -> UserOutput:
    current_user = get_current_user(token, user_service)
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
