from datetime import datetime
from pydantic import BaseModel





class MessageCreate(BaseModel):
    message: str


class Message(MessageCreate):
    # id: str
    user_id: str
    # created_at=datetime(2023, 10, 4, 21, 5, 52, 637000)
    created_at: datetime


class MessageResponse(Message):
    created_at: str  # Define the field as a string

# class MessageResponse(Message):
#     class Config:
#         exclude = ["created_at"]




class MessageRecipient(BaseModel):
    recipient_id: str
    chat_id: str

    
class ChatId(BaseModel):
    chat_id: str | None


class GroupChatCreate(ChatId):
    chat_name: str | None
    member_ids: list[str]
    messages: list[Message | None]


class ChatResponse(ChatId):
    member_ids: list[str]
    messages: list[Message | None]


class GroupChatResponse(GroupChatCreate):
    pass
