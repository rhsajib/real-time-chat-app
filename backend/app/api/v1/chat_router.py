from fastapi import status, Depends, APIRouter
from fastapi.responses import JSONResponse
from app.schemas import chat_schemas
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings

from app.database.chat_db import (
    db_get_all_private_msg_recipients,
    db_get_all_private_chats,
    db_get_messages,
    db_create_message,
    # db_create_private_chat,
    db_create_private_chat_id,
    db_get_existing_private_chat,
    db_get_recepient_chat_id,
    db_create_group_chat,
    db_get_private_chat_info
)


router = APIRouter()


"""
user2 2123bb0ec29d4471bd295be4cca68aed
user3 b3cea1638eb14ee48ec20d879f0789e4
user4 d4511f3932be45199ff23c4ae76faf96

"""


@router.get('/private/msg_recipients/', 
            status_code=status.HTTP_200_OK, 
            response_model=list[chat_schemas.MessageRecipient])
async def get_all_private_msg_recipients(db: AsyncIOMotorDatabase = Depends(get_db)):
    current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2
    recipients = await db_get_all_private_msg_recipients(current_user_id, db)
    return recipients


@router.get('/private/all/', 
            status_code=status.HTTP_200_OK, 
            response_model=list[chat_schemas.ChatResponse])
async def get_all_private_chats(db: AsyncIOMotorDatabase = Depends(get_db)):
    current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2
    chats = await db_get_all_private_chats(current_user_id, db)
    return chats


# Create private chat
# @router.get('/private/{recipient_id}',
# @router.get('/private/create/{recipient_id}',
#             status_code=status.HTTP_200_OK,
#             response_model=chat_schemas.ChatResponse)
# async def create_private_chat(recipient_id: str,
#                               db: AsyncIOMotorDatabase = Depends(get_db)):

#     current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2

#     if current_user_id == recipient_id:
#         content = {'message': 'self messaging is not available!!'}
#         return JSONResponse(content=content)

#     existing_chat = await db_get_existing_private_chat(current_user_id, recipient_id, db)
#     if existing_chat:
#         print('chat already exists')
#         # print(existing_chat)
#         return existing_chat

#     new_chat = await db_create_private_chat(current_user_id, recipient_id, db)
#     # print('new_chat', new_chat)
#     return new_chat


# Create private chat id
@router.get('/private/recipient/create_chat_id/{recipient_id}',
            status_code=status.HTTP_200_OK,
            response_model=chat_schemas.ChatId)
async def create_recipient_chat_id(recipient_id: str,
                              db: AsyncIOMotorDatabase = Depends(get_db)):

    current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2

    chat_id = await db_create_private_chat_id(current_user_id, recipient_id, db)
    return chat_id





# Get private chat id
@router.get('/private/recipient/get_chat_id/{recipient_id}',
            status_code=status.HTTP_200_OK,
            response_model=chat_schemas.ChatId)
async def get_recipient_chat_id(recipient_id: str,
                              db: AsyncIOMotorDatabase = Depends(get_db)):

    current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2

    chat_id = await db_get_recepient_chat_id(current_user_id, recipient_id, db)
    return chat_id



# Get private chat info
# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9
@router.get('/private/chat-info/{chat_id}',
            status_code=status.HTTP_200_OK,
            response_model=chat_schemas.ChatResponse)
async def get_private_chat_info(chat_id: str,
                        db: AsyncIOMotorDatabase = Depends(get_db)):

    chat_info = await db_get_private_chat_info(chat_id, db)
    return chat_info











# Get private chat messages
# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9
@router.get('/private/messages/{chat_id}',
            status_code=status.HTTP_200_OK,
            response_model=list[chat_schemas.Message])
async def get_private_messages(chat_id: str,
                               db: AsyncIOMotorDatabase = Depends(get_db)):

    messages = await db_get_messages(chat_id, db)
    return messages


# Create new private message
@ router.post('/private/message/create/{chat_id}',
              status_code=status.HTTP_201_CREATED,
              response_model=chat_schemas.Message)
async def create_private_message(chat_id: str,
                                 message_data: chat_schemas.MessageCreate,
                                 db: AsyncIOMotorDatabase = Depends(get_db)):

    # Access message_data.message to get the message from the request body
    message = message_data.message
    # get collection name for private chat
    db_collection = settings.PRIVATE_CHAT
    print(message)
    current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2
    message = await db_create_message(current_user_id, chat_id, message, db, db_collection)
    return message


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

    # messages = await db_get_messages(chat_id, db)
    # return messages


async def delete_chat():
    pass
