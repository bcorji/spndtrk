import uuid

import jwt

import pytest

from app.core.jwt import (
    create_access_token,
    decode_access_token,
)
from app.core.config import settings


def test_create_access_token():
    user_id = uuid.uuid4()

    token, expires_in = create_access_token(user_id)

    payload = decode_access_token(token)

    assert payload["sub"] == str(user_id)
    assert expires_in == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


def test_invalid_token():
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token("invalid.token.value")