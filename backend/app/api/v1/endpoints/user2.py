from fastapi import HTTPException, status, Depends, APIRouter
from app.exceptions import UserCreationError
from app import schemas
from app.database.db import get_db
from app.core.utils import get_password_hash
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.crud.user import (
    db_create_user,
    db_get_user_by_id,
    db_get_all_user,
    db_update_user,
    db_delete_user,
)


router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED, 
             response_model=schemas.User)
async def create_user(
        user_data: schemas.UserCreate,
        db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        if user_data.password1 != user_data.password2:
            raise UserCreationError("password", "Passwords do not match")

        # hash password
        password_hash = get_password_hash(user_data.password1)

        # Create a new dictionary with the original fields from user_data
        # and the new 'password' field
        # Set hashed password as user password
        # https://fastapi.tiangolo.com/tutorial/extra-models/
        updated_user_data = {
            **user_data.model_dump(),
            "password": password_hash
        }

        # def validate_unique_phone_number(cls, value):

        # Add new user to database
        new_user = await db_create_user(updated_user_data, db)

        # print(new_user)
        return new_user
    except UserCreationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail={"error": "Validation Failed", "errors": [
                                {"field": e.field, "message": e.message}]})


# Get current user data
@router.get('/info/me', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_current_user_detail(db: AsyncIOMotorDatabase = Depends(get_db)):
    current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2
    user = await db_get_user_by_id(current_user_id, db)
    return user


# Get a user data
@router.get('/info/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_user_detail(user_id: str,
                          db: AsyncIOMotorDatabase = Depends(get_db)):

    user = await db_get_user_by_id(user_id, db)
    return user


# Get all user
@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[schemas.User])
async def get_all_user(db: AsyncIOMotorDatabase = Depends(get_db)):
    users = await db_get_all_user(db)
    return users


# Update user data
@router.put('/update/info/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def update_user(
    user_id: str,
    updated_data: schemas.UserUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):

    user = await db_update_user(user_id, updated_data, db)
    return user


# Delete User
@router.delete('/delete/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_use(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    deleted_user = await db_delete_user(user_id, db)

    # return {'message': 'User deleted'}
    return deleted_user
