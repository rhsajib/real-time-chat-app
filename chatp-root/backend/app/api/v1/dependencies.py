from app.services.token import TokenManager
from app.crud.chat import GroupChatManager, PrivateChatManager
from app.crud.user import User
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from jose import JWTError, jwt
from app.exceptions import credentials_exception
from app import schemas


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V_STR}/login/access-token')


# Dependency to create a User instance
async def get_user_manager(db: AsyncIOMotorDatabase = Depends(get_db)):
    return User(db)


async def get_token_manager(
        user_manager: User = Depends(get_user_manager)
):
    return TokenManager(user_manager)


async def get_private_chat_manager(
    db: AsyncIOMotorDatabase = Depends(get_db),
    user_manager: User = Depends(get_user_manager)    # here User is a class
):
    return PrivateChatManager(db, user_manager)


async def get_group_chat_manager(
    db: AsyncIOMotorDatabase = Depends(get_db),
    user_manager: User = Depends(get_user_manager)    # here User is a class
):
    return GroupChatManager(db, user_manager)


# process 1
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        token_manager: TokenManager = Depends(get_token_manager),
) -> schemas.User:
    
    user = await token_manager.get_user_form_jwt_token(
        token,
        settings.ACCESS_TOKEN_SUBJECT_KEY
    )

    if not user:
            raise credentials_exception
    return user


# process 2

"""
    # in user_manager
    # the Depends object is to get the instance of the User class,
    # and then we call the get_by_id method on that instance
    async def get_user_form_jwt_token(
            token: str,
            user_manager: User
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

    async def get_current_user(
            token: str = Depends(oauth2_scheme),
            user_manager: User = Depends(get_user_manager)
    ) -> schemas.User:

        # print('token', token)
        user = await get_user_form_jwt_token(token, user_manager)
        return user
"""


# Process 3
# The following one is regular process to get ccurrent user
# But I followed the above one because i will use 'get_user_form_jwt_token'
# in the websocket section to get current user.
"""
    # in user_manager
    # the Depends object is to get the instance of the User class, 
    # and then we call the get_by_id method on that instance

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
"""


async def get_current_active_user(
        current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:

    if not current_user['is_active']:
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
