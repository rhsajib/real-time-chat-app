
from app.schemas import User, UserInDb



def user_serializer(user: dict) -> User:
    return User(**user)

