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


"""
user2 2123bb0ec29d4471bd295be4cca68aed
user3 b3cea1638eb14ee48ec20d879f0789e4
user4 d4511f3932be45199ff23c4ae76faf96

"""


# Create private chat
@router.get('/private/{recipient_id}',
             status_code=status.HTTP_200_OK,
             response_model=chat_schemas.ChatResponse)
async def get_private_chat(recipient_id: str,
                       db: AsyncIOMotorDatabase = Depends(get_db)):

    current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2

    if current_user_id == recipient_id:
        content = {'message': 'self messaging is not available!!'}
        return JSONResponse(content=content)
    
    # get collection name for private chat
    db_collection = settings.PRIVATE_CHAT

    existing_chat = await db_get_existing_chat(current_user_id, recipient_id, db, db_collection)
    if existing_chat:
        print('chat already exists')
        print(existing_chat)
        return existing_chat

    new_chat = await db_create_private_chat(current_user_id, recipient_id, db, db_collection)
    # print('new_chat', new_chat)
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

    current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2
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
    
    current_user_id = '7eb9b6bdf0a343e9857467436f692118'  # admin
    db_collection = settings.GROUP_CHAT
    group_data.member_ids.append(current_user_id)
    chat = await db_create_group_chat(group_data, db, db_collection)
    return chat




# Create new group message
# chat_id: c32beeb6e7be4e7fb597622e37041226
@ router.post('/group/message/send/{chat_id}', 
              status_code=status.HTTP_201_CREATED, 
              response_model=chat_schemas.Message)
async def create_group_message(chat_id: str,
                         message: str,
                         db: AsyncIOMotorDatabase = Depends(get_db)):
    
    # get collection name for group chat
    db_collection = settings.GROUP_CHAT

    current_user_id = '1549cdb3da5446868e21d9767b3e03cf'  # admin
    message = await db_create_message(current_user_id, chat_id, message, db, db_collection)
    return message




# Get all messages of a group chat 
# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9
@router.get('/group/messages/{chat_id}',
            status_code=status.HTTP_200_OK,
            response_model=list[chat_schemas.Message])
async def get_group_messages(chat_id: str,
                       db: AsyncIOMotorDatabase = Depends(get_db)):

    # get collection name for private chat
    db_collection = settings.GROUP_CHAT

    messages = await db_get_messages(chat_id, db, db_collection)
    return messages



async def delete_chat():
    pass

