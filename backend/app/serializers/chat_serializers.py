from app.models import chat
from app import schemas



def new_chat_serializer(member_ids):
    serialized_chat = schemas.PrivateChatModel(member_ids=member_ids)


def new_message_serializer(message: chat.Message) -> schemas.MessageResponse:
    # Serialize the datetime field to a string for the response
    created_at_str = message.created_at.isoformat()
    message.created_at = created_at_str
    print('new_message_serializer', message)
    return message
