from fastapi import Depends, HTTPException, status
from app import schemas
from datetime import datetime, timedelta
from app.core.config import settings
from app.exceptions import credentials_exception
from app.crud.user import User
from itsdangerous import URLSafeTimedSerializer
from jose import JWTError, jwt


class TokenManager:
    def __init__(self, user_manager: User):
        self.user_manager = user_manager
        self.jwt_secret_key = settings.JWT_SECRET_KEY
        self.jwt_algorithm = settings.ALGORITHM
        self.ts = URLSafeTimedSerializer(settings.ACTIVATION_SECRET_KEY)
        self.expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    async def get_jwt_access_token(self, subject: str) -> str:
        if self.expires_delta:
            expire = datetime.utcnow() + self.expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=20)

        to_encode = {"exp": expire, "sub": subject}

        encoded_jwt = jwt.encode(
            to_encode,
            self.jwt_secret_key,
            algorithm=self.jwt_algorithm
        )

        return encoded_jwt

    async def get_data_form_jwt_token(self, token) -> schemas.TokenPayload:
        try:
            payload = jwt.decode(
                token, self.jwt_secret_key,
                algorithms=[self.jwt_algorithm]
            )

            # print('payload', payload)

            subject: str = payload.get("sub")
            if subject is None:
                raise credentials_exception

            # token_data = schemas.TokenPayload(**payload)
            return payload
        except JWTError:
            raise credentials_exception

    async def get_user_form_jwt_token(self, token: str, subject_key: str) -> schemas.User:
        token_data = await self.get_data_form_jwt_token(token)
        # print('token_data', token_data)
        subject = token_data.get('sub')

        if subject_key == 'id':
            user = await self.user_manager.get_by_id(subject)
        elif subject_key == 'email':
            user = await self.user_manager.get_by_email(subject)

        if not user:
            raise credentials_exception
        return user

    async def generate_activation_token(self, email: str) -> str:
        return self.ts.dumps(email, salt="activation-salt")

    async def validate_activation_token(self, token: str) -> str:
        try:
            # Adjust max_age as needed
            loaded_email = self.ts.loads(
                token, 
                salt="activation-salt", 
                max_age=3600
            )
            # print('loaded_email:', loaded_email)
            return loaded_email
        except:
            return None
