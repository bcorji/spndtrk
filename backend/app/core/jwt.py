import uuid

from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


def create_access_token(
    user_id: uuid.UUID,
) -> tuple[str, int]:

    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    expire = datetime.now(timezone.utc) + timedelta(
        seconds=expires_in
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token, expires_in


def decode_access_token(token: str) -> dict:

    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        options={
            "require": ["sub", "exp", "iat"],
        },
    )