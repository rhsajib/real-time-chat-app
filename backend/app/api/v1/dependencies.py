from app.crud.chat import PrivateChatManager
from app.crud.user import User
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from jose import JWTError, jwt
from app.exceptions import credentials_exception
from app import schemas



oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/login/access-token')


# Dependency to create a User instance
async def get_user_manager(db: AsyncIOMotorDatabase = Depends(get_db)):
    return User(db)




async def get_private_chat_manager(db: AsyncIOMotorDatabase = Depends(get_db), 
                             user_manager: User = Depends(get_user_manager)):  # here User is a class
    return PrivateChatManager(db, user_manager)




async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_manager: User = Depends(get_user_manager)
) -> schemas.User:
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
    
    # except (jwt.JWTError, ValidationError):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Could not validate credentials",
    #     )

    user = await user_manager.get_by_id(token_data.sub)
    # print('get_current_user', user)
    if not user:
        raise credentials_exception
    return user



async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    
    if current_user['is_disabled']:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



async def get_current_active_superuser(
    current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:

    if not current_user['is_superuser']:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user