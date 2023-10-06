from app.models.chat_models import PrivateChatModel
from app.schemas.user_schemas import UserDetail, UserResponse
from app.schemas.chat_schemas import ChatId

def user_serializer(user) -> UserResponse:
    return UserDetail(**user)

def chat_id_serializer(chat_id) -> ChatId:
    return ChatId(chat_id=chat_id)

def new_chat_serializer(member_ids):
    serialized_chat = PrivateChatModel(member_ids=member_ids)