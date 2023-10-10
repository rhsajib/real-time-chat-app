from fastapi import HTTPException, status, Depends, APIRouter
from app.api.v1.dependencies import get_user_manager
from app.exceptions import UserCreationError
from app import schemas
from app.crud.user import User


router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED,
             response_model=schemas.User)
async def create_user(
        user_data: schemas.UserCreate,
        user_manager: User = Depends(get_user_manager)):
    try:
        if user_data.password1 != user_data.password2:
            raise UserCreationError("password", "Passwords do not match")

        # def validate_unique_phone_number(cls, value):

        # Create a new user using the User class
        new_user = await user_manager.create_user(user_data)

        # print(new_user)
        return new_user
    except UserCreationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail={"error": "Validation Failed", "errors": [
                                {"field": e.field, "message": e.message}]})


# Get current user data
@router.get('/info/me', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_current_user_detail(user_manager: User = Depends(get_user_manager)):
    current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2
    user = await user_manager.get_by_id(current_user_id)
    return user


# Get a user data
@router.get('/info/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_user_detail(user_id: str,
                          user_manager: User = Depends(get_user_manager)):

    user = await user_manager.get_by_id(user_id)
    return user


# Get all user
@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[schemas.User])
async def get_all_user(user_manager: User = Depends(get_user_manager)):
    users = await user_manager.get_all()
    return users


# Update user data
@router.put('/update/info/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def update_user(
    user_id: str,
    updated_data: schemas.UserUpdate,
    user_manager: User = Depends(get_user_manager)
):

    user = await user_manager.update_user(user_id, updated_data)
    return user


# Delete User
@router.delete('/delete/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_use(
    user_id: str,
    user_manager: User = Depends(get_user_manager)
):
    deleted_user = await user_manager.delete_user(user_id)

    # return {'message': 'User deleted'}
    return deleted_user