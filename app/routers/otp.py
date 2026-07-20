from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.core.otp import (
    generate_otp,
    get_otp_expiry,
    verify_otp,
    is_otp_expired
)

router = APIRouter(
    prefix="/otp",
    tags=["OTP"]
)


@router.post("/send")
def send_otp(
    email: str,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    otp = generate_otp()

    user.otp = otp
    user.otp_expiry = get_otp_expiry()

    db.commit()

    print("=" * 50)
    print(f"OTP for {user.email}: {otp}")
    print("=" * 50)

    return {
        "message": "OTP generated successfully"
    }


@router.post("/verify")
def verify_user_otp(
    email: str,
    otp: str,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.otp is None:
        raise HTTPException(
            status_code=400,
            detail="OTP not generated"
        )

    if is_otp_expired(user.otp_expiry):
        raise HTTPException(
            status_code=400,
            detail="OTP expired"
        )

    if not verify_otp(
        user.otp,
        otp
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    user.is_verified = True
    user.otp = None
    user.otp_expiry = None

    db.commit()

    return {
        "message": "OTP verified successfully"
    }