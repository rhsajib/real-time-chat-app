from fastapi import APIRouter

from app.api.v1.endpoints import user, chat, auth


api_router = APIRouter()

# Api Routers
api_router.include_router(auth.router, tags=['Auth'], prefix='/auth')
api_router.include_router(user.router, tags=['User'], prefix='/user')
api_router.include_router(chat.router, tags=['Chat'], prefix='/chat')

