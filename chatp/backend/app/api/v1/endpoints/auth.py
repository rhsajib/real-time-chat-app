from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v1.dependencies import get_user_manager
from app import schemas
from app.core.config import settings
from app.crud.user import User 
from app.core.security import get_access_token


router = APIRouter()



@router.post('/login/access-token', response_model=schemas.Token)
async def login_access_token(user_data: schemas.Login, 
                             user_manager: User = Depends(get_user_manager)) -> Any:
    print(user_data)
    user = await user_manager.authenticate(user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = get_access_token(user.get('id'), expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
