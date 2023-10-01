
from app.models.models import UserModel
from fastapi import status, HTTPException
from app.schemas import user_schemas
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.exceptions import UserCreationError


# Get a user from database
async def db_get_user(
    user_id: str,
    db: AsyncIOMotorDatabase
) -> user_schemas.User:

    user = await db['Users'].find_one({'id': user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User not found')

    return user


# Create a new user in database
async def db_create_user(
    user: user_schemas.UserCreate,
    db: AsyncIOMotorDatabase
) -> user_schemas.User:
    
    try:
        new_user = UserModel(**user.model_dump())
        result = await db['Users'].insert_one(new_user.model_dump())

        # Check if the user creation was successful
        if result.acknowledged:
            created_user = await db_get_user(new_user.id, db)
            return created_user
        else:
            # Raise the custom exception with a specific error message
            raise UserCreationError("User creation failed, write operation not acknowledged")

    except UserCreationError as e:
        # Handle the custom exception
        print(f"User creation error: {str(e)}")

    except Exception as e:
        # Handle other exceptions if needed
        print(f"An unexpected error occurred: {str(e)}")



# Update user data in database
async def db_update_user(
    user_id: str,
    updated_data: user_schemas.UserUpdate,
    db: AsyncIOMotorDatabase
) -> user_schemas.User:


    existing_user = await db['Users'].find_one({'id': user_id})

    print(existing_user)

    if existing_user:
        result = await db['Users'].update_one(
            {'id': user_id}, {'$set': updated_data.model_dump()}
        )

        # Check if the update was successful
        if result.modified_count == 1:
            # If the update was successful, return the updated user data
            updated_user = await db_get_user(user_id, db)
            return updated_user
        


