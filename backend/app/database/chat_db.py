from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.chat_models import MessageModel, MessageRecipientModel, PrivateChatModel
from .user_db import db_get_user


async def is_chat_member(user_id: str, chat_id: str, db: AsyncIOMotorDatabase) -> bool:
    chat = get_chat(chat_id, db)
    if user_id in chat.get('members'):
        return True
    return False


async def get_chat(chat_id: str,
                   db: AsyncIOMotorDatabase):
    chat = await db['PrivateChat'].find_one({'chat_id': chat_id})
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Chat not found')
    return chat


async def update_sent_messages_recipients(user_id, recipient, db):
    result = await db['Users'].update_one(
        {'id': user_id},
        {'$push': {'sent_messages_recipients': recipient}}
    )
    if result.matched_count == 1 and result.modified_count == 1:
        return True


async def add_chat_id_to_user(member_ids: list, chat_id: str, db: AsyncIOMotorDatabase):
    """In member ids, one is user another is recipient"""
    user1, user2 = recipient2, recipient1 = member_ids

    # serialization
    user1_recipient1 = MessageRecipientModel(
        recipient_id=recipient1, chat_id=chat_id)

    user2_recipient2 = MessageRecipientModel(
        recipient_id=recipient2, chat_id=chat_id)

    update1 = await update_sent_messages_recipients(user1, user1_recipient1.model_dump(), db)
    update2 = await update_sent_messages_recipients(user2, user2_recipient2.model_dump(), db)

    if update1 and update2:
        return True


async def db_get_existing_chat(current_user_id: str,
                               recipient_id: str,
                               db: AsyncIOMotorDatabase):
    query = {
        'id': current_user_id,
        'sent_messages_recipients.recipient_id': recipient_id
    }

    # Retrieve the user with the matching query
    user = await db['Users'].find_one(query)

    if user:
        for recipients in user['sent_messages_recipients']:
            if recipients['recipient_id'] == recipient_id:
                chat_id = recipients['chat_id']
                chat = await get_chat(chat_id, db)
                return chat

    return []


async def db_create_private_chat(current_user_id: str,
                                recipient_id: str,
                                db: AsyncIOMotorDatabase):

    member_ids = [current_user_id, recipient_id]
    serialized_chat = PrivateChatModel(member_ids=member_ids)

    result = await db['PrivateChat'].insert_one(serialized_chat.model_dump())

    if result.acknowledged:
        # add chat_id to member's sent_messages_recipients field
        added = await add_chat_id_to_user(member_ids, serialized_chat.chat_id, db)

        if added:
            created_chat = await get_chat(serialized_chat.chat_id, db)
            # print('created_chat', created_chat)
            return created_chat

    # except Exception as e:
    #     # Handle other exceptions if needed
    #     print(f"An unexpected error occurred: {str(e)}")


async def db_get_messages(chat_id: str, db: AsyncIOMotorDatabase):
    chat = await get_chat(chat_id, db)
    return chat.get('messages')



async def db_create_message(current_user_id: str,
                            chat_id: str, 
                            message: str,
                            db: AsyncIOMotorDatabase):

    serialized_message = MessageModel(user_id=current_user_id, message=message)
    print(serialized_message)
    print(serialized_message.model_dump())
    result = await db['PrivateChat'].update_one(
        {'chat_id': chat_id},
        {'$push':{'messages': serialized_message.model_dump()}}
    )


    if result.matched_count == 1 and result.modified_count == 1:
        # return {"message": "Item added to profile successfully"}
        return serialized_message.model_dump()

