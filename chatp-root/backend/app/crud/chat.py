from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from app.crud.user import User
# from app.crud.user import db_get_user_by_id
from app.models import (
    GroupChatModel,
    MessageModel,
    MessageRecipientModel,
    PrivateChatModel)
from app import schemas
from app.serializers import serializers


# async def is_chat_member(user_id: str, chat_id: str, db: AsyncIOMotorDatabase) -> bool:
#     chat = db_get_chat(chat_id, db)
#     if user_id in chat.get('members'):
#         return True
#     return False



GROUP_CHAT_COLLECTION = settings.GROUP_CHAT_COLLECTION


class BaseChatManager:
    def __init__(self, db: AsyncIOMotorDatabase, chat_collection: str , user_manager: User):
        self.db = db
        self.chat_collection = self.db[chat_collection]
        self.user_manager = user_manager

    async def get_chat_by_id(self, chat_id: str) -> dict:
        chat = await self.chat_collection .find_one({'chat_id': chat_id})
        if not chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Chat not found')
        return chat

    async def get_chat_messages(self, chat_id: str) -> list[schemas.Message]:
        chat = await self.get_chat_by_id(chat_id)
        return chat['messages']

    async def get_chats_from_ids(self, chat_ids: list[str]) -> list:
        # Query the collection for matching chat_ids
        matched_chats = await self.chat_collection.find(
            {'chat_id': {'$in': chat_ids}}
        ).to_list(None)
        return matched_chats

    async def insert_chat_to_db(self, new_chat) -> bool:
        result = await self.chat_collection.insert_one(new_chat.model_dump())
        if result.acknowledged:
            return True
        return False

    async def create_message(
        self,
        current_user_id: str,
        chat_id: str,
        message: str,
    ) -> schemas.Message:

        chat = await self.get_chat_by_id(chat_id)

        if current_user_id not in chat.get('member_ids'):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Message was not sent!'
            )

        new_message = MessageModel(created_by=current_user_id, message=message)
        print('new_message', new_message)

        result = await self.chat_collection.update_one(
            {'chat_id': chat_id},
            {'$push': {'messages': new_message.model_dump()}}
            # as I pushed new message inside messages,
            # it will not create any default '_id' for new message
            # if i use insert_one(), it will automatically create a '_id' field
        )

        if result.matched_count == 1 and result.modified_count == 1:
            # return {"message": "Item added to profile successfully"}
            return new_message


class PrivateChatManager(BaseChatManager):
    def __init__(self, db: AsyncIOMotorDatabase, user_manager: User):
        super().__init__(db, settings.PRIVATE_CHAT_COLLECTION, user_manager)

    async def update_message_recipients(
        self,
        user_id: str,
        recipient_model: schemas.MessageRecipient
    ):
        result = await self.user_manager.update_one(
            {'id': user_id},
            {'$push': {'private_message_recipients': recipient_model.model_dump()}}
        )
        if result.matched_count == 1 and result.modified_count == 1:
            return True

    async def create_chat(
        self,
        current_user_id: str,
        recipient_id: str
    ) -> schemas.PrivateChat:

        ids = [current_user_id, recipient_id]
        new_chat = PrivateChatModel(member_ids=ids)
        # print('new_chat', new_chat)

        inserted = await self.insert_chat_to_db(new_chat)
        # print('inserted', inserted)

        if not inserted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Chat not created.')

        # In member ids, one is user another is recipient
        # user1, recipient1  = recipient2, user2 = ids
        # message_recipient = [(user1, recipient1), (user2, recipient2)]
        # (user, recipient)
        message_recipients = [(ids[0], ids[1]), (ids[1], ids[0])]

        for user_id, recipient_id in message_recipients:
            recipient_model = MessageRecipientModel(
                recipient_id=recipient_id, chat_id=new_chat.chat_id)
            print('recipient_model', recipient_model)

            # add chat_id to member's private_message_recipients field
            insertd = await self.user_manager.insert_private_message_recipient(
                user_id, recipient_model
            )
            if not insertd:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Message recipient was not added to user.'
                )

        return new_chat

    async def get_all_msg_recipients(self, user_id: str) -> list[schemas.MessageRecipient]:
        user = await self.user_manager.get_by_id(user_id)
        if user:
            return user["private_message_recipients"]
        return []

    async def get_all_chats(self, user_id: str):
        user = await self.user_manager.get_by_id(user_id)
        if user:
            chat_ids = [recipient['chat_id']
                        for recipient in user.get('private_message_recipients')]
            return await self.get_chats_from_ids(chat_ids)
        return []
    
    async def get_recipiet_id_from_chat_members(self, member_ids: list[str], current_user_id: str):

        recipiet_id = member_ids[0] if member_ids[1] == current_user_id else member_ids[1]
        return recipiet_id
    
    
    async def get_recipient_profile(self, member_ids: list[str], current_user_id:str) -> schemas.User:
        recipient_id = await self.get_recipiet_id_from_chat_members(member_ids, current_user_id)
        user = await self.user_manager.get_by_id(recipient_id)
        return user
    
    async def get_recepient(
            self, 
            current_user_id: str, 
            recipient_id: str
    ) -> schemas.MessageRecipient:
        # query = {
        #     'id': current_user_id,
        #     'private_message_recipients.recipient_id': recipient_id
        # }
        # Retrieve the user with the matching query
        # user = await self.chat_collection.find_one(query)

        user = await self.user_manager.get_by_id(current_user_id)

        # print('user[\'private_message_recipients\']: ', user['private_message_recipients'] )
        if user['private_message_recipients']:
            for recipient in user['private_message_recipients']:
                if recipient['recipient_id'] == recipient_id:
                    return recipient
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No private message recipients!'
        )


"""------------------------Section: handle private chat------------------------"""


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


class GroupChatManager(BaseChatManager):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, settings.GROUP_CHAT_COLLECTION)


async def get_group_chat(chat_id: str,
                         db: AsyncIOMotorDatabase):
    chat = await db['GroupChat'].find_one({'chat_id': chat_id})
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Chat not found')
    return chat


async def db_create_group_chat(group_data: schemas.GroupChat,
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


"""------------------------Section: handle messages------------------------"""
# Section: handle messages


async def db_get_messages(chat_id: str, db: AsyncIOMotorDatabase):
    chat = await db_get_chat(chat_id, db, collection=PRIVATE_CHAT_COLLECTION)
    return chat.get('messages')
