from app.crud.user import User
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends



# Dependency to create a User instance
def get_user_manager(db: AsyncIOMotorDatabase = Depends(get_db)):
    return User(db)
