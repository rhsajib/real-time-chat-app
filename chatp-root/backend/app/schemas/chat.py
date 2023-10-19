from datetime import datetime
from pydantic import BaseModel


class MessageBase(BaseModel):
    message: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: str
    created_by: str
    # created_at=datetime(2023, 10, 4, 21, 5, 52, 637000)
    created_at: datetime
  

class MessageResponse(Message):
    created_at: str          # Define the field as a string
 

# class MessageResponse(Message):
#     class Config:
#         exclude = ["created_at"]


class ChatId(BaseModel):
    chat_id: str


class MessageRecipient(ChatId):
    recipient_id: str


class ChatBase(ChatId):
    member_ids: list[str]
    messages: list[Message | None]
    type: str


class PrivateChat(ChatBase):
    pass


class PrivateChatResponse(ChatBase):
    pass



class GroupChat(ChatBase):
    chat_name: str | None


class GroupChatResponse(GroupChat):
    pass
