from fastapi import status, Depends, APIRouter
from fastapi.responses import JSONResponse
from app.schemas import chat_schemas
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.chat_db import (
    db_get_messages,
    db_create_message,
    db_create_private_chat,
    db_get_existing_chat
)


router = APIRouter()









# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9    username=newuser
@router.post('/{recipient_id}/private-chat',
             status_code=status.HTTP_201_CREATED,
             response_model=chat_schemas.ChatResponse)
async def private_chat(recipient_id: str,
                      db: AsyncIOMotorDatabase = Depends(get_db)):

    # current_user_id = 'e88bc66a7f6a400aae013cad7700e1d7'  # admin
    current_user_id = '8766afaf17bf42fc8970400e4d35ebb9'  # admin

    if current_user_id == recipient_id:
        content = {'message': 'self messaging is not available!!'}
        return JSONResponse (content=content)
    
    existing_chat = await db_get_existing_chat(current_user_id, recipient_id, db)
    if existing_chat:
        print('chat already exists')
        print(existing_chat)
        return existing_chat

    new_chat = await db_create_private_chat(current_user_id, recipient_id, db)
    print('new_chat', new_chat)
    return new_chat
    
        





# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9
@router.get('/{chat_id}/messages',
            status_code=status.HTTP_200_OK,
            response_model=list)
async def get_messages(chat_id: str,
                       db: AsyncIOMotorDatabase = Depends(get_db)):

    messages = await db_get_messages(chat_id, db)
    return messages




# Create new message
# chat_id: c32beeb6e7be4e7fb597622e37041226
@ router.post('/{chat_id}/create-message', status_code=status.HTTP_201_CREATED, response_model=chat_schemas.Message)
async def create_message(chat_id: str,
                         message = str,
                         db: AsyncIOMotorDatabase = Depends(get_db)):

    current_user_id = '8766afaf17bf42fc8970400e4d35ebb9'  # admin
    message = await db_create_message(current_user_id, chat_id, message, db)
    return message
