from pydantic import BaseModel, EmailStr
from datetime import datetime

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
    updated: datetime
    active: bool


