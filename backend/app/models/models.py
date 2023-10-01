from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
from ..core.utils import(
    datetime_now, 
    get_uuid4
)


class UserModel(BaseModel):
    id: UUID = Field(default_factory=get_uuid4)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    username: str = Field(..., max_length=20)
    email: EmailStr = Field(..., max_length=50)
    password: str = Field(...) 
    created_at: datetime = Field(default_factory=datetime_now)
    updated: datetime = Field(default_factory=datetime_now)
    active: bool = False



    class Config:
        # allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "password123",
                "created_at": "2023-09-30T12:00:00",
                "updated": "2023-09-30T12:00:00",
                "active": True
            }
        }
    
    @classmethod
    def __repr__(cls):
        return f'{cls.first_name}'


