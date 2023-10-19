from fastapi import status, Depends, APIRouter, HTTPException
from app import schemas
from app.schemas import shared
from app.api.v1.dependencies import get_current_user, get_private_chat_manager, get_current_active_user
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings

from app.crud.chat import PrivateChatManager
from app.serializers.chat_serializers import message_serializer


router = APIRouter()



@router.get('/home',
            status_code=status.HTTP_200_OK,
            response_model=schemas.User)
async def get_authenticated_user(current_user: schemas.User = Depends(get_current_active_user)):
    print('current_user form get_authenticated_user', current_user)
    return current_user


@router.get('/private/msg-recipients/',
            status_code=status.HTTP_200_OK,
            response_model=list[schemas.MessageRecipient])
async def get_all_private_message_recipients(
    pvt_chat_manager: PrivateChatManager = Depends(get_private_chat_manager),
    current_user: schemas.User = Depends(get_current_active_user)
):

    recipients = await pvt_chat_manager.get_all_msg_recipients(current_user['id'])
    return recipients


# Get private chat info
# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9
@router.get('/private/info/{chat_id}',
            status_code=status.HTTP_200_OK,
            response_model=shared.PrivateChatResponseWithRecipient)
async def get_private_chat(
    chat_id: str,
    pvt_chat_manager: PrivateChatManager = Depends(get_private_chat_manager),
    current_user: schemas.User = Depends(get_current_active_user)
):

    chat = await pvt_chat_manager.get_chat_by_id(chat_id)
    # print('chat', chat)
    if chat['messages']:
        # serialize chat messages
        serialized_messages = [message_serializer(msg) for msg in chat['messages']]
        chat['messages'] = serialized_messages
    

    recipient_profile = await pvt_chat_manager.get_recipient_profile(
        chat['member_ids'], current_user['id']
    )
    print('recipient_profile', recipient_profile)
    chat['user_id'] = current_user['id']
    chat['recipient_profile'] = recipient_profile
    return chat

# Get private chat recipient


@router.get('/private/recipient/chat-id/{recipient_id}',
            status_code=status.HTTP_200_OK,
            response_model=schemas.ChatId)
async def get_recipient_chat_id(
    recipient_id: str,
    pvt_chat_manager: PrivateChatManager = Depends(get_private_chat_manager),
    current_user: schemas.User = Depends(get_current_active_user)
):

    # current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2
    try:
        recipient = await pvt_chat_manager.get_recepient(current_user['id'], recipient_id)
        return recipient
    except HTTPException as e:
        raise e


@router.get('/private/all/',
            status_code=status.HTTP_200_OK,
            response_model=list[schemas.PrivateChatResponse])
async def get_all_private_chats(
    pvt_chat_manager: PrivateChatManager = Depends(get_private_chat_manager),
    current_user: schemas.User = Depends(get_current_active_user)
):
    # current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2
    chats = await pvt_chat_manager.get_all_chats(current_user['id'])
    return chats


# Create private chat
@router.get('/private/recipient/create-chat/{recipient_id}',
            status_code=status.HTTP_201_CREATED,
            response_model=schemas.PrivateChat)
async def create_private_chat(
    recipient_id: str,
    pvt_chat_manager: PrivateChatManager = Depends(get_private_chat_manager),
    current_user: schemas.User = Depends(get_current_active_user)
):

    try:
        created_chat = await pvt_chat_manager.create_chat(current_user['id'], recipient_id)
        return created_chat
    except HTTPException as e:
        raise e


# Get private chat messages
@router.get('/private/messages/{chat_id}',
            status_code=status.HTTP_200_OK,
            response_model=list[schemas.Message])
async def get_private_messages(
    chat_id: str,
    pvt_chat_manager: PrivateChatManager = Depends(get_private_chat_manager),
    current_user: schemas.User = Depends(get_current_active_user)
):

    messages = await pvt_chat_manager.get_chat_messages(chat_id)
    return messages


# Create new private message
@ router.post('/private/message/create/{chat_id}',
              status_code=status.HTTP_201_CREATED,
              response_model=schemas.Message)
async def create_private_message(chat_id: str,
                                 message_data: schemas.MessageCreate,
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
             response_model=schemas.GroupChatResponse)
async def create_group_chat(group_data: schemas.GroupChat,
                            db: AsyncIOMotorDatabase = Depends(get_db)):

    current_user_id = '7eb9b6bdf0a343e9857467436f692118'  # admin
    db_collection = settings.GROUP_CHAT_COLLECTION
    group_data.member_ids.append(current_user_id)
    chat = await db_create_group_chat(group_data, db, db_collection)
    return chat


# Create new group message
# chat_id: c32beeb6e7be4e7fb597622e37041226
@ router.post('/group/message/send/{chat_id}',
              status_code=status.HTTP_201_CREATED,
              response_model=schemas.Message)
async def create_group_message(chat_id: str,
                               message: str,
                               db: AsyncIOMotorDatabase = Depends(get_db)):

    # get collection name for group chat
    db_collection = settings.GROUP_CHAT_COLLECTION

    current_user_id = '1549cdb3da5446868e21d9767b3e03cf'  # admin
    message = await db_create_message(current_user_id, chat_id, message, db, db_collection)
    return message


# Get all messages of a group chat
# recipient_id = 8766afaf17bf42fc8970400e4d35ebb9
@router.get('/group/messages/{chat_id}',
            status_code=status.HTTP_200_OK,
            response_model=list[schemas.Message])
async def get_group_messages(chat_id: str,
                             db: AsyncIOMotorDatabase = Depends(get_db)):

    # get collection name for private chat
    db_collection = settings.GROUP_CHAT_COLLECTION

    # messages = await db_get_messages(chat_id, db)
    # return messages


async def delete_chat():
    pass
