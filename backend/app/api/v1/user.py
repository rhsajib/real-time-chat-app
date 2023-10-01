from fastapi import status, HTTPException, Depends, APIRouter
from app.database.user_db import db_create_user
from app.schemas import user_schemas
from app.database.db import get_db
from app.core.utils import get_password_hash
from motor.motor_asyncio import AsyncIOMotorDatabase




router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=user_schemas.User)
async def create_user(user: user_schemas.UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):

    # print(user.email)
    # print(user.model_dump().get('email'))

    # hash password
    password_hash = get_password_hash(user.password)

    # Set hashed password as user password    
    user.password = password_hash

    # Add new user to database
    new_user = await db_create_user(user, db)
    
    # print(new_user)
    return new_user
