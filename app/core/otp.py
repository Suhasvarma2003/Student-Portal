import random
from datetime import datetime, timedelta

OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5


def generate_otp() -> str:

    return "".join(
        random.choices(
            "0123456789",
            k=OTP_LENGTH
        )
    )


def get_otp_expiry():

    return datetime.utcnow() + timedelta(
        minutes=OTP_EXPIRY_MINUTES
    )


def is_otp_expired(expiry_time):

    return datetime.utcnow() > expiry_time


def verify_otp(
    stored_otp: str,
    entered_otp: str
):

    return stored_otp == entered_otp