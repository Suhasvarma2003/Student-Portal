import resend

from app.core.config import (
    RESEND_API_KEY,
    RESEND_FROM_EMAIL
)

resend.api_key = RESEND_API_KEY


def send_otp_email(
    recipient: str,
    otp: str
):

    resend.Emails.send(
        {
            "from": RESEND_FROM_EMAIL,
            "to": recipient,
            "subject": "Email Verification OTP",
            "html": f"""
                <h2>Email Verification</h2>

                <p>Your OTP is:</p>

                <h1>{otp}</h1>

                <p>This OTP is valid for 5 minutes.</p>
            """
        }
    )