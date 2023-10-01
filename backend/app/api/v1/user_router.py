from fastapi import status, Depends, APIRouter
from app.schemas import user_schemas
from app.database.db import get_db
from app.core.utils import get_password_hash
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database.user_db import (
    db_create_user, 
    db_get_user, 
    db_update_user
)




router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=user_schemas.User)
async def create_user(
    user: user_schemas.UserCreate, 
    db: AsyncIOMotorDatabase = Depends(get_db)):

    # print(user.email)
    # print(user.model_dump().get('email'))

    # hash password
    password_hash = get_password_hash(user.password)

    # Set hashed password as user password    
    user.password = password_hash

    # def validate_unique_phone_number(cls, value):

    # Add new user to database
    new_user = await db_create_user(user, db)
    
    # print(new_user)
    return new_user



# Get user data
@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=user_schemas.User)
async def get_user(user_id: str, 
                   db: AsyncIOMotorDatabase = Depends(get_db)):
    
    user = await db_get_user(user_id, db)
    return user


# Update user data
@router.put('/update/{user_id}', status_code=status.HTTP_200_OK, response_model=user_schemas.User)
# @router.put('/update/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id: str, 
                      updated_data: user_schemas.UserUpdate,
                      db: AsyncIOMotorDatabase = Depends(get_db)):
    
    user = await db_update_user(user_id, updated_data, db)
    return user

