import pytest
from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def test_decode_valid_token():
    payload = {"sub": "12345", "role": "user"}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    decoded = decode_and_validate(token)
    assert decoded["sub"] == "12345"

def test_decode_invalid_token():
    with pytest.raises(ValueError):
        decode_and_validate("invalid.token.here")