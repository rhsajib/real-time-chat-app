from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.schemas.chat import MessageRecipient


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str
    
# Properties to receive via API on creation
class UserCreate(UserBase):
    password1: str
    password2: str

# Additional properties to return via API
class User(UserBase):
    id: str  
    first_name: str | None
    last_name: str | None
    phone: str | None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_disabled: bool
    is_superuser: bool 


# Properties to receive via API on update
class UserUpdate(User):
    password: str | None
    
# Additional properties stored in DB
class UserInDb(UserUpdate):
    # disabled: bool  for disabling the account 
    private_message_recipients: list[MessageRecipient | None]
    group_chat_ids: list[str | None]




class UserOfAll(UserBase):
    id: str

