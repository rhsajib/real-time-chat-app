from .chat import PrivateChatResponse
from .user import User



class PrivateChatResponseWithRecipient(PrivateChatResponse):
    user_id: str
    recipient_profile: User