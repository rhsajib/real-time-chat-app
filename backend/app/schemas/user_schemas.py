from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.chat_schemas import MessageRecipient


class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    first_name: str | None
    last_name: str | None
    phone: str | None

class User(UserUpdate):
    id: str
    created_at: datetime
    updated_at: datetime
    active: bool
    private_message_recipients: list[MessageRecipient | None]
    group_chat_ids: list[str | None]

