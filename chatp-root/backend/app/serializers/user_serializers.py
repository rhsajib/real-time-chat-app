from app import schemas


def user_serializer(user: dict) -> schemas.User:
    return schemas.User(**user)

