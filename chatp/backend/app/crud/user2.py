
from app.serializers import serializers
from app.models.user import UserModel
from fastapi import status, HTTPException
from app import schemas
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.exceptions import UserCreationError
from app.core.config import settings


USERS_COLLECTION = settings.USERS_COLLECTION




# Get a user from database
async def db_get_user_by_id(user_id: str, db: AsyncIOMotorDatabase) -> dict:
    user = await db[USERS_COLLECTION].find_one({'id': user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User not found')
    return user


# Get all user from database
async def db_get_all_user(db: AsyncIOMotorDatabase):
    cursor = db[USERS_COLLECTION].find({})
    # to_list to retrieve the documents as a list
    users = await cursor.to_list(length=None)

    serialized_users = []
    for user in users:
        serialized_user = serializers.user_serializer(user)
        serialized_users.append(serialized_user)

    # print('serialized_users', serialized_users)
    return serialized_users


# Create a new user in database
async def db_create_user(user: dict, db: AsyncIOMotorDatabase) -> dict:
    try:
        new_user = UserModel(**user)
        print(new_user)

        result = await db[USERS_COLLECTION].insert_one(new_user.model_dump())

        # Check if the user creation was successful
        if result.acknowledged:
            created_user = await db_get_user_by_id(new_user.id, db)
            return created_user
        else:
            # Raise the custom exception with a specific error message
            raise UserCreationError(
                "User creation failed, write operation not acknowledged")

    except UserCreationError as e:
        # Handle the custom exception
        print(f"User creation error: {str(e)}")

    except Exception as e:
        # Handle other exceptions if needed
        print(f"An unexpected error occurred: {str(e)}")


# Update user data in database
async def db_update_user(
        user_id: str,
        updated_data: schemas.UerUpdate,
        db: AsyncIOMotorDatabase):

    existing_user = await db_get_user_by_id(user_id, db)

    result = await db[USERS_COLLECTION].update_one(
        {'id': user_id}, {'$set': updated_data.model_dump()}
    )

    # Check if the update was successful
    if result.modified_count == 1:
        # If the update was successful, return the updated user data
        updated_user = await db_get_user_by_id(user_id, db)
        return updated_user


# Delete user from database
async def db_delete_user(
        user_id: str,
        db: AsyncIOMotorDatabase):

    user = await db_get_user_by_id(user_id, db)
    deleted_user = await db[USERS_COLLECTION].delete_one({'id': user_id})
    if deleted_user.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'User not deleted')

    # user['_id'] deleted because
    # MongoDB's ObjectId cannot be directly serialized to JSON.
    # we should convert the ObjectId to a string or delete it before
    # returning it as part of the user object.
    # otherwise it will cause error
    del user['_id']
    print('user', user)
    return user
