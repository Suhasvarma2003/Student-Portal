import random
from datetime import datetime, timedelta


OTP_EXPIRE_MINUTES = 5


def generate_otp():
    return str(random.randint(100000, 999999))


def get_otp_expiry():
    return datetime.utcnow() + timedelta(
        minutes=OTP_EXPIRE_MINUTES
    )