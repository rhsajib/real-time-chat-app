from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, root_validator
from app.schemas.chat import MessageRecipient
from ..core.utils import(
    datetime_now, 
    get_uuid4
)



class UserModel(BaseModel):
    id: str = Field(default_factory=get_uuid4)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    username: str = Field(..., max_length=20)
    email: EmailStr = Field(..., max_length=50)
    phone: str | None =Field(None, max_length=30)
    password: str = Field(...) 
    created_at: datetime = Field(default_factory=datetime_now)
    updated_at: datetime = Field(default_factory=datetime_now)
    is_active: bool = False
    is_disabled: bool = False     
    is_superuser: bool = False                                                    # for disabling the account
    private_message_recipients: list[MessageRecipient | None] = Field([])   # it will store ids of the recipients
    group_chat_ids: list[str | None] = Field([])



    # add email, username validator

    # @root_validator(skip_on_failure=True)
    # def one_of_email_or_mobile_must_be_present(cls, values: dict) -> dict:
    #     assert values["email"] != None or values["mobile"] != None, "either one of email or mobile must be present"
    #     return values


    # @validator("email")
    # async def validate_unique_email(cls, value):
    #     existing_user = await db["Users"].find_one({"email": value})
    #     if existing_user:
    #         raise HTTPException(status_code=400, detail="Email already registered")
    #     return value

    # @validator("profession", pre=True)
    # def set_default_profession(cls, val: str) -> str:
    #     if not val:
    #         return OTHER

    #     return val.strip().lower()



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


