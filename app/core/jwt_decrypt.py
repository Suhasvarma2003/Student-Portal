from jose import jwt, JWTError

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

security = HTTPBearer()


def decode_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


def get_current_user(

    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),

    db: Session = Depends(get_db)

):

    token = credentials.credentials

    payload = decode_token(token)

    email = payload.get("sub")

    if not email:

        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user