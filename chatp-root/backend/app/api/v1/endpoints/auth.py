from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from app.api.v1.dependencies import get_token_manager, get_user_manager
from app import schemas
from app.core.config import settings
from app.schemas.user import UserUpdate
from app.services.token import TokenManager
from app.crud.user import User 



router = APIRouter()
FRONTEND_LOGIN_URL = settings.FRONTEND_LOGIN_URL

@router.post('/login/access-token', response_model=schemas.Token)
async def login_access_token(
    user_data: schemas.Login, 
    user_manager: User = Depends(get_user_manager),
    token_manager: TokenManager= Depends(get_token_manager)
) -> Any:
    print(user_data)
    user = await user_manager.authenticate(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect email or password"
        )
    
    if not user.get('is_active'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Please activate your account before login.'
        )
    
    # token subject will be required for getting access token
    jwt_token_subject = user.get(settings.ACCESS_TOKEN_SUBJECT_KEY)
    # inthis case it is like user.get('id')

    access_token = await token_manager.get_jwt_access_token(jwt_token_subject)

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
  
    # Validate the activation token

    user_email = await token_manager.validate_activation_token(activation_token)

    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid activation token."
        ) 
    
    user = await user_manager.get_by_email(user_email)
    user['is_active'] = True
    
    # this is for filtering user update data so that all data can't be updated
    user_update_instance = UserUpdate(**user)
    active_user = await user_manager.update_user(user_update_instance)

    if active_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request.'
        )

    # print('active_user', active_user)
    # Provide the URL to redirect to the login page
    redirect_url = f"{FRONTEND_LOGIN_URL}/?activated=true"  # Adjust the path as needed
    #  redirect_url = f"{FRONTEND_LOGIN_URL}/login?activated=true"

    # process 1
    # ref https://stackoverflow.com/questions/70656412/how-to-redirect-to-dynamic-url-inside-a-fastapi-endpoint
    # ref https://medium.com/featurepreneur/fastapi-render-template-redirection-c98a26ae1e2a
    return RedirectResponse(redirect_url)

  