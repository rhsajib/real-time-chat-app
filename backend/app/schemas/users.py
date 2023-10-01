from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password_hash: str

class User(UserBase):
    id: UUID
    created_at = datetime
    active: bool
