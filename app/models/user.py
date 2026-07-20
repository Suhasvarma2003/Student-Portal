from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String,
        unique=True,
        index=True
    )

    hashed_password = Column(String)

    otp = Column(String,nullable=True)

    otp_expiry = Column(DateTime,nullable=True)

    is_verified = Column(Boolean,default=False)