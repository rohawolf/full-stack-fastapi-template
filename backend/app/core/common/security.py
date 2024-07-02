from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.core.config import settings


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    delta_ = expires_delta or timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = datetime.now(UTC) + delta_
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM
    )
