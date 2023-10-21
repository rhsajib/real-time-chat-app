from fastapi import HTTPException, status, Depends, APIRouter
from app.api.v1.dependencies import(
     get_token_manager, 
     get_current_active_user, 
     get_user_manager, 
     get_current_user
)
from app.exceptions import UserCreationError
from app import schemas
from app.crud.user import User
from app.services.token import TokenManager
from app.services.worker.tasks import send_account_activation_email


router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED,
             response_model=schemas.User)
async def create_user(
        user_data: schemas.UserCreate,
        user_manager: User = Depends(get_user_manager),
        token_manager: TokenManager = Depends(get_token_manager)
        # current_user: schemas.User = Depends(get_current_active_user)
        # if i use current user here, it will raise '401 Unauthorized'
):
    try:
        if user_data.password1 != user_data.password2:
            raise UserCreationError("password", "Passwords do not match")

        # Create a new user using the User class
        new_user = await user_manager.create_user(user_data)
        # print(new_user)

        # Send account activation email to new 

        recipient_email = new_user.get('email')
        activation_token = await token_manager.generate_activation_token(recipient_email)
        send_account_activation_email.delay(activation_token, recipient_email)
        return new_user
        # print('result', result, dir(result))

        # Wait for the Celery task to complete and get the result
        # result_value = result.get()     # same as result_value = AsyncResult(result.id).get()
        
        # Retrieve the result of the task once it's completed
        # result_value = result.get()
        # if result_value:
        # return new_user
            # return {"message": "Task triggered", "task_id": result.id}
            # return {"message": "Task triggered", "task_id": result.id, "result": result_value}

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
@router.get('/info/{user_id}', 
            status_code=status.HTTP_200_OK, 
            response_model=schemas.User)
async def get_user_detail(user_id: str,
                          user_manager: User = Depends(get_user_manager),
                          current_user: schemas.User = Depends(get_current_active_user)):

    user = await user_manager.get_by_id(user_id)
    # print('user', user)
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
