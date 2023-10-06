from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from app.database.user_db import db_get_user
from app.models.chat_models import (
    GroupChatModel,
    MessageModel,
    MessageRecipientModel,
    PrivateChatModel)
from app.schemas import chat_schemas
from app.serializers import serializers


# async def is_chat_member(user_id: str, chat_id: str, db: AsyncIOMotorDatabase) -> bool:
#     chat = db_get_chat(chat_id, db)
#     if user_id in chat.get('members'):
#         return True
#     return False

# async


USER_CCOLLECTION = settings.USERS
PRIVATE_CHAT_COLLECTION = settings.PRIVATE_CHAT
GROUP_CHAT_COLLECTION = settings.GROUP_CHAT


async def db_get_chat(chat_id: str,
                      db: AsyncIOMotorDatabase,
                      collection: str | None = None):

    chat = await db[collection].find_one({'chat_id': chat_id})
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Chat not found')
    return chat


async def db_get_existing_private_chat(current_user_id: str,
                                       recipient_id: str,
                                       db: AsyncIOMotorDatabase,
                                       ):
    query = {
        'id': current_user_id,
        'private_message_recipients.recipient_id': recipient_id
    }

    # Retrieve the user with the matching query

    user = await db[USER_CCOLLECTION].find_one(query)

    if user:
        for recipient in user['private_message_recipients']:
            if recipient['recipient_id'] == recipient_id:
                chat_id = recipient['chat_id']
                chat = await db_get_chat(chat_id, db, collection=PRIVATE_CHAT_COLLECTION)
                return chat

    return []


async def db_get_recepient_chat_id(current_user_id: str,
                                   recipient_id: str,
                                   db: AsyncIOMotorDatabase):
    query = {
        'id': current_user_id,
        'private_message_recipients.recipient_id': recipient_id
    }

    # Retrieve the user with the matching query

    user = await db[USER_CCOLLECTION].find_one(query)

    chat_id = None
    if user:
        for recipient in user['private_message_recipients']:
            if recipient['recipient_id'] == recipient_id:
                chat_id = recipient['chat_id']

    serialized_chat_id = serializers.chat_id_serializer(chat_id)

    return serialized_chat_id.model_dump()


"""------------------------Section: handle private chat------------------------"""


async def update_private_message_recipients(user_id, recipient, db):
    result = await db[USER_CCOLLECTION].update_one(
        {'id': user_id},
        {'$push': {'private_message_recipients': recipient}}
    )
    if result.matched_count == 1 and result.modified_count == 1:
        return True


async def add_chat_id_to_users(member_ids: list, chat_id: str, db: AsyncIOMotorDatabase):
    """In member ids, one is user another is recipient"""
    user1, user2 = recipient2, recipient1 = member_ids

    # serialization
    user1_recipient1 = MessageRecipientModel(
        recipient_id=recipient1, chat_id=chat_id)

    user2_recipient2 = MessageRecipientModel(
        recipient_id=recipient2, chat_id=chat_id)

    update1 = await update_private_message_recipients(user1, user1_recipient1.model_dump(), db)
    update2 = await update_private_message_recipients(user2, user2_recipient2.model_dump(), db)

    if update1 and update2:
        return True


async def db_create_private_chat_id(current_user_id: str,
                                    recipient_id: str,
                                    db: AsyncIOMotorDatabase):

    member_ids = [current_user_id, recipient_id]
    new_chat = PrivateChatModel(member_ids=member_ids)

    result = await db[PRIVATE_CHAT_COLLECTION].insert_one(new_chat.model_dump())

    if result.acknowledged:
        # add chat_id to member's private_message_recipients field
        added = await add_chat_id_to_users(member_ids, new_chat.chat_id, db)

        if added:
            serialized_chat_id = serializers.chat_id_serializer(
                new_chat.chat_id)
            return serialized_chat_id.model_dump()


async def db_get_all_private_msg_recipients(user_id: str, db: AsyncIOMotorDatabase):
    user = await db_get_user(user_id, db)
    if user:
        return user["private_message_recipients"]
    return []


async def db_get_private_chat_info(chat_id: str, db: AsyncIOMotorDatabase):
    chat = await db_get_chat(chat_id, db, collection=PRIVATE_CHAT_COLLECTION)
    return chat


async def db_get_all_private_chats(user_id: str, db: AsyncIOMotorDatabase):
    user = await db_get_user(user_id, db)

    if user:
        # Get the list of chat IDs from the user's private_message_recipients
        chat_ids = [recipient['chat_id']
                    for recipient in user.get('private_message_recipients')]

        # Query the PRIVATE_CHAT_COLLECTION collection for matching chat_ids
        matched_chats = await db[PRIVATE_CHAT_COLLECTION].find(
            {'chat_id': {'$in': chat_ids}}
        ).to_list(None)

        return matched_chats

    return []

"""
async def db_create_private_chat(current_user_id: str,
                                 recipient_id: str,
                                 db: AsyncIOMotorDatabase,
                                 ):

    member_ids = [current_user_id, recipient_id]
    serialized_chat = PrivateChatModel(member_ids=member_ids)

    result = await db[PRIVATE_CHAT_COLLECTION].insert_one(serialized_chat.model_dump())

    if result.acknowledged:
        # add chat_id to member's private_message_recipients field
        added = await add_chat_id_to_users(member_ids, serialized_chat.chat_id, db)

        if added:
            created_chat = await db_get_chat(serialized_chat.chat_id, db, collection=PRIVATE_CHAT_COLLECTION)
            # print('created_chat', created_chat)
            return created_chat

    # except Exception as e:
    #     # Handle other exceptions if needed
    #     print(f"An unexpected error occurred: {str(e)}")

"""



"""------------------------Section: handle group chat------------------------"""


async def get_group_chat(chat_id: str,
                         db: AsyncIOMotorDatabase):
    chat = await db['GroupChat'].find_one({'chat_id': chat_id})
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Chat not found')
    return chat


async def db_create_group_chat(group_data: chat_schemas.GroupChatCreate,
                               db: AsyncIOMotorDatabase,
                               collection):
    serialized_chat = GroupChatModel(**group_data.model_dump())
    result = await db[collection].insert_one(serialized_chat.model_dump())

    if result.acknowledged:
        # add chat_id to every member's group_chat_ids
        added = await add_group_chat_id_to_users(serialized_chat.chat_id,
                                                 serialized_chat.member_ids, db)
        if added:
            chat = await get_group_chat(serialized_chat.chat_id, db)
            return chat


async def add_group_chat_id_to_users(chat_id: str,
                                     member_ids: list[str],
                                     db: AsyncIOMotorDatabase) -> bool:
    for id in member_ids:
        result = await db['Users'].update_one(
            {'id': id},
            {'$push': {'group_chat_ids': chat_id}}
        )
        if result.matched_count != 1 and result.modified_count != 1:
            content = {
                'message': 'Group chat id was not added to user id: {id}'}
            return JSONResponse(content=content)
    return True


# Section: handle messages
async def db_get_messages(chat_id: str, db: AsyncIOMotorDatabase):
    chat = await db_get_chat(chat_id, db, collection=PRIVATE_CHAT_COLLECTION)
    return chat.get('messages')


async def db_create_message(current_user_id: str,
                            chat_id: str,
                            message: str,
                            db: AsyncIOMotorDatabase,
                            collection: str):

    chat = await db_get_chat(chat_id, db, collection)

    if current_user_id not in chat.get('member_ids'):
        return JSONResponse(content={'message': 'message was not sent'})

    serialized_message = MessageModel(user_id=current_user_id, message=message)
    # print(serialized_message)
    # print(serialized_message.model_dump())
    result = await db[collection].update_one(
        {'chat_id': chat_id},
        {'$push': {'messages': serialized_message.model_dump()}}
    )

    if result.matched_count == 1 and result.modified_count == 1:
        # return {"message": "Item added to profile successfully"}
        return serialized_message.model_dump()
