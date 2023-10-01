from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
from ..core.utils import(
    datetime_now, 
    get_uuid4,
    get_password_hash
)


class User(BaseModel):
    id: UUID = Field(default_factory=get_uuid4)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    username: str = Field(..., max_length=20)
    email: str = EmailStr
    password_hash: str = Field(default_factory=get_password_hash) 
    created_at: datetime = Field(default_factory=datetime_now)
    updated: datetime = Field(default_factory=datetime_now)
    active: bool = True


