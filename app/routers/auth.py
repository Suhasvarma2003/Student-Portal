from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

from app.core.security import (
    hash_password,
    verify_password
)

from app.core.jwt_encrypt import (
    create_access_token
)

from app.schemas.password import (
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from app.core.otp import (
    generate_otp,
    get_otp_expiry,
    verify_otp,
    is_otp_expired
)

from app.core.email import send_otp_email

router = APIRouter()


@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        hashed_password=hash_password(
            user.password
        )
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered"
    }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    if not db_user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email first."
        )

    token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout():

    return {
        "message":
        "Logout successful. Delete token on client side."
    }


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == request.email)
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

    send_otp_email(
        recipient=user.email,
        otp=otp
    )

    return {
        "message":
        "Password reset OTP sent successfully."
    }


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == request.email)
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

        # Clear expired OTP
        user.otp = None
        user.otp_expiry = None
        db.commit()

        raise HTTPException(
            status_code=400,
            detail="OTP expired. Please request a new OTP."
        )

    if not verify_otp(
        user.otp,
        request.otp
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    # Prevent using the same password again
    if verify_password(
        request.new_password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="New password cannot be the same as the old password."
        )

    # Update password
    user.hashed_password = hash_password(
        request.new_password
    )

    # Clear OTP after successful reset
    user.otp = None
    user.otp_expiry = None

    db.commit()

    return {
        "message": "Password reset successfully."
    }