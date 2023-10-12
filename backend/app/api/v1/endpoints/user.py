from fastapi import HTTPException, status, Depends, APIRouter
from app.api.v1.dependencies import get_current_active_user, get_user_manager, get_current_user
from app.exceptions import UserCreationError
from app import schemas
from app.crud.user import User


router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED,
             response_model=schemas.User)
async def create_user(
        user_data: schemas.UserCreate,
        # current_user: schemas.User = Depends(get_current_active_user)
        user_manager: User = Depends(get_user_manager),
        # if i use current user here, it will raise '401 Unauthorized'
):
    try:
        if user_data.password1 != user_data.password2:
            raise UserCreationError("password", "Passwords do not match")

        # Create a new user using the User class
        new_user = await user_manager.create_user(user_data)

        # print(new_user)
        return new_user
    except UserCreationError as e:
        print(e)
        print(e.field, e.message)

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                'error': 'Validation Field',
                'errors': [
                    {
                        'field': e.field,
                        'message': e.message
                    }
                ]
            }
        )



# Get current user data
@router.get('/info/me', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_current_user_detail(
    user_manager: User = Depends(get_user_manager),
    current_user: schemas.User = Depends(get_current_active_user)
):

    # return current_user
    user = await user_manager.get_by_id(current_user['id'])
    return user


# Get a user data
@router.get('/info/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_user_detail(user_id: str,
                          user_manager: User = Depends(get_user_manager),
                          current_user: schemas.User = Depends(get_current_active_user)):

    user = await user_manager.get_by_id(user_id)
    return user


# Get all user
@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[schemas.UserOfAll])
async def get_all_user(user_manager: User = Depends(get_user_manager),
                       current_user: schemas.User = Depends(get_current_active_user)):
    users = await user_manager.get_all_except_me(current_user['id'])
    return users


# Update user data
@router.put('/update/info/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def update_user(
    user_id: str,
    updated_data: schemas.UserUpdate,
    user_manager: User = Depends(get_user_manager),
    current_user: schemas.User = Depends(get_current_active_user)
):

    user = await user_manager.update_user(user_id, updated_data)
    return user


# Delete User
@router.delete('/delete/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_use(
    user_id: str,
    user_manager: User = Depends(get_user_manager),
    current_user: schemas.User = Depends(get_current_active_user)
):
    deleted_user = await user_manager.delete_user(user_id)

    # return {'message': 'User deleted'}
    return deleted_user
