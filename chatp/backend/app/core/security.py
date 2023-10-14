from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.core.config import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



# Convert pain password to hashed password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Verify a plain password by matching with hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_access_token(subject: str, expires_delta: timedelta):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)
    
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
