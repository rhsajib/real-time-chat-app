from datetime import datetime
from app.schemas.chat_schemas import Message
from pydantic import BaseModel, Field, EmailStr, root_validator
from ..core.utils import(
    datetime_now, 
    get_uuid4
)

class MessageRecipientModel(BaseModel):
    recipient_id: str = Field(...)
    chat_id: str = Field(...)


class MessageModel(BaseModel):
    # message_id: str = Field(default_factory=get_uuid4)
    user_id: str = Field(...)
    message: str = Field(...)
    created_at: datetime = Field(default_factory=datetime_now)

class MessageResponseModel(MessageModel):
    @property
    def created_at_str(self):
        # Convert the datetime to a string
        return self.created_at.isoformat()       # Created At (Formatted): 2023-10-04T21:05:52.637000


class PrivateChatModel(BaseModel):
    chat_id: str = Field(default_factory=get_uuid4)
    member_ids: list[str] = Field(...)
    messages: list[Message | None] = Field([])

class GroupChatModel(PrivateChatModel):
    chat_name: str | None = Field(None)


