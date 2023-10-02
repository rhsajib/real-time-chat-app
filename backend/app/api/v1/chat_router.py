from fastapi import status, Depends, APIRouter
from fastapi.responses import JSONResponse
from app.schemas import chat_schemas
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings

from app.database.chat_db import (
    db_get_messages,
    db_create_message,
    db_create_private_chat,
    db_get_existing_chat,
    db_create_group_chat
)


router = APIRouter()





# Create private chat
# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9    username=newuser
@router.post('/private/create/{recipient_id}',
             status_code=status.HTTP_201_CREATED,
             response_model=chat_schemas.ChatResponse)
async def create_private_chat(recipient_id: str,
                       db: AsyncIOMotorDatabase = Depends(get_db)):

    current_user_id = 'e88bc66a7f6a400aae013cad7700e1d7'  # admin

    if current_user_id == recipient_id:
        content = {'message': 'self messaging is not available!!'}
        return JSONResponse(content=content)

    existing_chat = await db_get_existing_chat(current_user_id, recipient_id, db)
    if existing_chat:
        print('chat already exists')
        return existing_chat

    new_chat = await db_create_private_chat(current_user_id, recipient_id, db)
    print('new_chat', new_chat)
    return new_chat




# Create new private message
@ router.post('/private/message/create/{chat_id}', 
              status_code=status.HTTP_201_CREATED, 
              response_model=chat_schemas.Message)
async def create_private_message(chat_id: str,
                         message: str,
                         db: AsyncIOMotorDatabase = Depends(get_db)):
    
    # get collection name for private chat
    db_collection = settings.PRIVATE_CHAT

    current_user_id = '8766afaf17bf42fc8970400e4d35ebb9'  # admin
    message = await db_create_message(current_user_id, chat_id, message, db, db_collection)
    return message




# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9
@router.get('/private/messages/{chat_id}',
            status_code=status.HTTP_200_OK,
            response_model=list[chat_schemas.Message])
async def get_private_messages(chat_id: str,
                       db: AsyncIOMotorDatabase = Depends(get_db)):

    # get collection name for private chat
    db_collection = settings.PRIVATE_CHAT

    messages = await db_get_messages(chat_id, db, db_collection)
    return messages






# Create group chat
@router.post('/group/create',
             status_code=status.HTTP_201_CREATED, 
             response_model=chat_schemas.GroupChatResponse)
async def create_group_chat(group_data: chat_schemas.GroupChatCreate,
                            db: AsyncIOMotorDatabase = Depends(get_db)):
    
    current_user_id = 'e88bc66a7f6a400aae013cad7700e1d7'  # admin
    group_data.member_ids.append(current_user_id)
    chat = await db_create_group_chat(group_data, db)
    return chat




# Create new group message
# chat_id: c32beeb6e7be4e7fb597622e37041226
@ router.post('/group/message/create/{chat_id}', 
              status_code=status.HTTP_201_CREATED, 
              response_model=chat_schemas.Message)
async def create_group_message(chat_id: str,
                         message: str,
                         db: AsyncIOMotorDatabase = Depends(get_db)):
    
    # get collection name for group chat
    db_collection = settings.GROUP_CHAT

    current_user_id = '8766afaf17bf42fc8970400e4d35ebb9'  # admin
    message = await db_create_message(current_user_id, chat_id, message, db, db_collection)
    return message




# Get all messages of a group chat 
# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9
@router.get('/group/messages/{chat_id}',
            status_code=status.HTTP_200_OK,
            response_model=list[chat_schemas.Message])
async def get_private_messages(chat_id: str,
                       db: AsyncIOMotorDatabase = Depends(get_db)):

    # get collection name for private chat
    db_collection = settings.GROUP_CHAT

    messages = await db_get_messages(chat_id, db, db_collection)
    return messages





