from app.schemas.user_schemas import User

def user_serializer(user) -> User:
    return User(**user)