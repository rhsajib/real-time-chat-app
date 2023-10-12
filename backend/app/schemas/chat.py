from datetime import datetime
from pydantic import BaseModel

class MessageBase(BaseModel):
    message: str
    
class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    created_by: str  
    created_at: datetime    # created_at=datetime(2023, 10, 4, 21, 5, 52, 637000)


class MessageResponse(Message):
    created_at: str          # Define the field as a string

# class MessageResponse(Message):
#     class Config:
#         exclude = ["created_at"]



class ChatId(BaseModel):
    chat_id: str


class MessageRecipient(ChatId):
    recipient_id: str
    # chat_id: str


class ChatBase(ChatId):
    # chat_id: str
    member_ids: list[str]
    messages: list[Message | None]

class PrivateChatCreate(ChatBase):
    pass

class PrivateChatResponse(ChatBase):
    pass

class GroupChatCreate(ChatBase):
    chat_name: str | None

class GroupChatResponse(GroupChatCreate):
    pass
