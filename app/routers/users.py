from fastapi import APIRouter, Depends

from app.models.user import User

from app.core.jwt_decrypt import (
    get_current_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_me(

    current_user: User = Depends(
        get_current_user
    )

):

    return {
        "id": current_user.id,
        "email": current_user.email
    }   