from fastapi import Depends
from app import schemas
from app.core.config import settings
from app.exceptions import credentials_exception
from app.crud.user import User
from jose import JWTError, jwt


class JwtTokenManager:
    def __init__(self, user_manager: User):
        self.user_manager = user_manager
    
    async def get_user_form_jwt_token(self, token) -> schemas.User:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            id: str = payload.get("sub")
            if id is None:
                raise credentials_exception

            token_data = schemas.TokenPayload(**payload)
        except JWTError:
            raise credentials_exception

        user = await self.user_manager.get_by_id(token_data.sub)
        # print('get_current_user', user)
        if not user:
            raise credentials_exception
        
        return user