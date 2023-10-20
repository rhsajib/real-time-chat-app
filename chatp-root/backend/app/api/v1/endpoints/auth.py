from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from app.api.v1.dependencies import get_token_manager, get_user_manager
from app import schemas
from app.core.config import settings
from app.crud.auth import TokenManager
from app.crud.user import User 
from app.core.security import get_access_token, is_valid_activation_token


router = APIRouter()

REACT_LOGIN_URL = "http://localhost:5173"

@router.post('/login/access-token', response_model=schemas.Token)
async def login_access_token(
    user_data: schemas.Login, 
    user_manager: User = Depends(get_user_manager),
    token_manager: TokenManager= Depends(get_token_manager)
) -> Any:
    print(user_data)
    user = await user_manager.authenticate(user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect email or password")
    
    access_token = await token_manager.get_access_token(user.get('id'))

    # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = get_access_token(user.get('id'), expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}



@router.get('/account/activate/{activation_token}')
async def activate_account(
    # request: Request,
    activation_token: str,
    user_manager: User = Depends(get_user_manager),
    token_manager: TokenManager = Depends(get_token_manager)
):
    try:
        # Validate the activation token
        print('activation_token', activation_token)
        user_email = await token_manager.validate_activation_token(activation_token)
        print('user_email', user_email)


        # Provide the URL to redirect to the login page
        redirect_url = f"{REACT_LOGIN_URL}"  # Adjust the path as needed
        #  redirect_url = f"{REACT_LOGIN_URL}/login?activated=true"


        # process 1
        # ref https://stackoverflow.com/questions/70656412/how-to-redirect-to-dynamic-url-inside-a-fastapi-endpoint
        # ref https://medium.com/featurepreneur/fastapi-render-template-redirection-c98a26ae1e2a
        return RedirectResponse(redirect_url)

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing the activation."
        ) from e


 # if user_email is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail='Invalid activation token'
        #     )
        #  # Activate the user's account in your database
        # user = await user_manager.get_by_email(user_email)
        # user.is_active = True
        # user.save()
        # print('activated user', user)
        