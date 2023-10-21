from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import settings


JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACTIVATION_SECRET_KEY = settings.ACTIVATION_SECRET_KEY

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ts = URLSafeTimedSerializer(ACTIVATION_SECRET_KEY)


# Convert pain password to hashed password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Verify a plain password by matching with hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)







# def get_access_token(subject: str, expires_delta: timedelta) -> str:
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=20)

#     to_encode = {"exp": expire, "sub": subject}
#     encoded_jwt = jwt.encode(
#         to_encode, JWT_SECRET_KEY, algorithm= ALGORITHM)
#     return encoded_jwt


# Activation token during signup
# def generate_activation_token(email: str) -> str:
#     return ts.dumps(email, salt="activation-salt")


# def is_valid_activation_token(token: str, email: str) -> bool:
#     try:
#         # Adjust max_age as needed
#         loaded_email = ts.loads(token, salt="activation-salt", max_age=3600)
#         print('loaded_email:', loaded_email )
#         return loaded_email == email
#     except:
#         return False
