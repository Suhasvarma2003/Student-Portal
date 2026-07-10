import random
from datetime import datetime, timedelta

OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5


def generate_otp():
    """
    Generate a numeric OTP.
    """
    return "".join(
        random.choices("0123456789", k=OTP_LENGTH)
    )


def get_otp_expiry():
    """
    Returns the OTP expiry time.
    """
    return datetime.utcnow() + timedelta(
        minutes=OTP_EXPIRY_MINUTES
    )


def is_otp_expired(expiry_time):
    """
    Check whether the OTP has expired.
    """
    return datetime.utcnow() > expiry_time