
from app.core.security import get_password_hash, verify_password
from app.serializers import serializers
from app.models.user import UserModel
from fastapi import status, HTTPException
from app import schemas
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.exceptions import UserCreationError
from app.core.config import settings


class BaseUserManager:
    '''
    Initialize the BaseUserManager.

    Args:
        db (AsyncIOMotorDatabase): The MongoDB database instance.
    '''

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.user_collection = self.db[settings.USERS_COLLECTION]

    async def get_by_id(self, id: str) -> schemas.UserInDb:
        user = await self.user_collection.find_one({'id': id})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User not found')
        return user

    async def get_by_email(self, email: str) -> schemas.UserInDb:
        user = await self.user_collection.find_one({'email': email})
        return user

    async def get_all(self) -> list[schemas.User]:
        cursor = self.user_collection.find({})
        # to_list to retrieve the documents as a list
        users = await cursor.to_list(length=None)

        serialized_users = []
        # as every user has default mongodb _id field, we can not directly export the _id.
        # so we need to serialize it
        for user in users:
            serialized_user = serializers.user_serializer(user)
            serialized_users.append(serialized_user)

        # print('serialized_users', serialized_users)
        return serialized_users

    async def get_all_except_me(self, current_user_id: str) -> list[schemas.User]:
        all_users = await self.get_all()
        # print(all_users)
        return [user for user in all_users if user.id != current_user_id]

    async def insert_private_message_recipient(
            self,
            user_id: str,
            recipient_model: schemas.MessageRecipient
    ):
        result = await self.user_collection.update_one(
            {'id': user_id},
            {'$push': {'private_message_recipients': recipient_model.model_dump()}}
        )
        if result.matched_count == 1 and result.modified_count == 1:
            return True
        # raise HTTPException

    # async def is_disabled(self, user: schemas.User) -> bool:
    #     return user.is_disabled

    # async def is_superuser(self, user: schemas.User) -> bool:
    #     return user.is_superuser


class UserDBManager(BaseUserManager):
    async def authenticate(self, user_data: schemas.Login) -> schemas.UserInDb:
        user = await self.get_by_email(user_data.email)
        # print('user', user)
        if not user:
            return None
        elif not verify_password(user_data.password, user.get('password')):
            return None
        return user


class UserCreator(BaseUserManager):
    async def create_user(self, user_data: schemas.UserCreate) -> schemas.User:
        try:
            # Check if email is already in use
            existing_user = await self.get_by_email(user_data.email)
            if existing_user:
                raise UserCreationError('Email', 'Email already in use!')

            # # Check if phone number is already in use
            # existing_user = await self.get_by_phone(user_data.phone)
            # if existing_user:
            #     raise UserCreationError('Phone', 'Phone number already in use')

            # Hash password
            password_hash = get_password_hash(user_data.password1)

            # Create a new dictionary with the original fields from user_data
            # and the new 'password' field
            # Set hashed password as user password
            # https://fastapi.tiangolo.com/tutorial/extra-models/
            updated_user_data = {
                **user_data.model_dump(),
                'password': password_hash
            }
            new_user = UserModel(**updated_user_data)
            print('new_user', new_user)

            result = await self.user_collection.insert_one(new_user.model_dump())
            # Check if the user creation was successful
            if result.acknowledged:
                created_user = await self.get_by_id(new_user.id)
                return created_user
            else:
                # Raise the custom exception with a specific error message
                raise UserCreationError(
                    'User creation failed', 'write operation not acknowledged')

        except UserCreationError as e:
            raise e

        # except Exception as e:
        #     return e
        #     # Handle other exceptions if needed
        #     print(f'An unexpected error occurred: {str(e)}')


class UserUpdater(BaseUserManager):
    '''
    Update user data in the database.

    Args:
        id (str): The user's ID.
        updated_data (schemas.UserUpdate): The updated user data.

    Returns:
        dict: The updated user data.
    '''
    async def update_user(
        self,
        updated_data: schemas.UserUpdate
    ) -> schemas.UserInDb | None:
        
        # mycollection.update_one(myquery, newvalues)
        result = await self.user_collection.update_one(
            {'id': updated_data.id},
            {'$set': updated_data.model_dump()}
        )
        # print(result.modified_count)
        # print(result.matched_count)
        # Check if the document was matched and modified
        if result.matched_count == 1 and result.modified_count == 1:
            # If the update was successful, return the updated user data
            updated_user = await self.get_by_id(updated_data.id)
            return updated_user
        return None


# Delete user from database


class UserDeleter(BaseUserManager):
    '''
    Delete a user from the database.

    Args:
        id (str): The user's ID to be deleted.

    Returns:
        dict: The deleted user data.
    Raises:
        HTTPException: If the user is not deleted.
    '''
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
        print('deleted user', user)
        return user


class User(UserDBManager, UserCreator, UserUpdater, UserDeleter):
    pass
