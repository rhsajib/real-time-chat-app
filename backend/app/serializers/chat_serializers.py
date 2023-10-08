from app.models import chat_models
from app.schemas import chat_schemas


def chat_id_serializer(chat_id) -> chat_schemas.ChatId:
    return chat_schemas.ChatId(chat_id=chat_id)


def new_chat_serializer(member_ids):
    serialized_chat = chat_models.PrivateChatModel(member_ids=member_ids)


def new_message_serializer(message: chat_schemas.Message) -> chat_schemas.MessageResponse:
    # Serialize the datetime field to a string for the response
    created_at_str = message.created_at.isoformat()
    message.created_at = created_at_str
    print('new_message_serializer', message)
    return message
