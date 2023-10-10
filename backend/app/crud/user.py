
from app.core.security import get_password_hash, verify_password
from app.serializers import serializers
from app.models.user import UserModel
from fastapi import status, HTTPException
from app import schemas
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.exceptions import UserCreationError
from app.core.config import settings


class BaseUserManager:
    """
    Initialize the BaseUserManager.

    Args:
        db (AsyncIOMotorDatabase): The MongoDB database instance.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = settings.USERS_COLLECTION
        self.user_collection = self.db[self.collection]

    async def get_by_id(self, id: str) -> schemas.UserInDb:
        """
        Get a user by their ID from the database.

        Args:
            id (str): The user's ID.

        Returns:
            dict: The user data.
        Raises:
            HTTPException: If the user is not found.
        """
        user = await self.user_collection.find_one({'id': id})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User not found')
        return user
    


    async def get_by_email(self, email: str) -> schemas.UserInDb:
        user = await self.user_collection.find_one({'email': email})
        return user


    async def get_all(self) -> list[schemas.User]:
        """
        Get all users from the database.

        Returns:
            list[schemas.User]: A list of user data.
        """
        cursor = self.user_collection.find({})
        # to_list to retrieve the documents as a list
        users = await cursor.to_list(length=None)

        serialized_users = []
        for user in users:
            serialized_user = serializers.user_serializer(user)
            serialized_users.append(serialized_user)

        # print('serialized_users', serialized_users)
        return serialized_users
    
    



class UserDBManager(BaseUserManager):
    async def authenticate(self, user_data: schemas.Login) -> schemas.UserInDb:
        user = await self.get_by_email(user_data.email)
        # print('user', user)
        if not user:
            return None
        if not verify_password(user_data.password, user.get('password')):
            return None
        return user


class UserCreator(BaseUserManager):
    async def create_user(self, user_data: schemas.UserCreate) -> schemas.User:
        try:
            # Hash password
            password_hash = get_password_hash(user_data.password1)

            # Create a new dictionary with the original fields from user_data
            # and the new 'password' field
            # Set hashed password as user password
            # https://fastapi.tiangolo.com/tutorial/extra-models/
            updated_user_data = {
                **user_data.model_dump(),
                "password": password_hash
            }
            new_user = UserModel(**updated_user_data)
            print(new_user)

            result = await self.user_collection.insert_one(new_user.model_dump())
            # Check if the user creation was successful
            if result.acknowledged:
                created_user = await self.get_by_id(new_user.id)
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



class UserUpdater(BaseUserManager):
    """
    Update user data in the database.

    Args:
        id (str): The user's ID.
        updated_data (schemas.UserUpdate): The updated user data.

    Returns:
        dict: The updated user data.
    """
    async def update_user(self, id: str, updated_data: schemas.UserUpdate):
        # existing_user = await self.get_by_id(id)

        result = await self.user_collection.update_one(
            {'id': id},
            {'$set': updated_data.model_dump()}
        )

        # Check if the update was successful
        if result.modified_count == 1:
            # If the update was successful, return the updated user data
            updated_user = await self.get_by_id(id)
            return updated_user

# Delete user from database


class UserDeleter(BaseUserManager):
    """
    Delete a user from the database.

    Args:
        id (str): The user's ID to be deleted.

    Returns:
        dict: The deleted user data.
    Raises:
        HTTPException: If the user is not deleted.
    """
    async def delete_user(self, id: str):
        user = await self.get_by_id(id)
        deleted_user = await self.user_collection.delete_one({'id': id})

        if deleted_user.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='User not deleted')

        # user['_id'] deleted because
        # MongoDB's ObjectId cannot be directly serialized to JSON.
        # we should convert the ObjectId to a string or delete it before
        # returning it as part of the user object.
        # otherwise it will cause error
        del user['_id']
        print('user', user)
        return user


class User(UserDBManager, UserCreator, UserUpdater, UserDeleter):
    pass
