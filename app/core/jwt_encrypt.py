from datetime import datetime, timedelta
from jose import jwt

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


def create_access_token(data: dict) -> str:

    payload = data.copy()

    expiration_time = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload["exp"] = expiration_time

    encoded_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_token