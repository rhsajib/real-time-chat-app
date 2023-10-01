
from datetime import datetime, timezone
from uuid import UUID, uuid4
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


#  Get current time
def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


# Generate a random UUID
def get_uuid4() -> UUID:
    return uuid4().hex


# Convert pain password to hashed password
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Verify a plain password by matching with hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
