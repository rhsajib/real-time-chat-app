from app.models.chat import MessageModel
from app import schemas



def new_chat_serializer(member_ids):
    serialized_chat = schemas.PrivateChatModel(member_ids=member_ids)


def message_serializer(message: MessageModel) -> schemas.MessageResponse:
    # Serialize the datetime field to a string for the response
    created_at_str = message.created_at.isoformat()
    message.created_at = created_at_str

    # Serialize the _id field to a string for the response
    message["_id"] = str(message["_id"])
    
    print('serialized_message', message)
    return message
