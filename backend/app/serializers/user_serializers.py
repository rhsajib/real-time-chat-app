
from app.schemas import user_schemas 


def user_serializer(user) -> user_schemas.UserResponse:
    return user_schemas.UserDetail(**user)

