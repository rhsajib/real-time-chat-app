from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    first_name: str | None
    last_name: str | None
    created_at: datetime
    updated: datetime
    active: bool
