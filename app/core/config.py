import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "your_secret_key_here"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

RESEND_FROM_EMAIL = os.getenv(
    "RESEND_FROM_EMAIL",
    "onboarding@resend.dev"
)