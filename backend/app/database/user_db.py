from app.models.models import UserModel
from app.schemas import user_schemas
from motor.motor_asyncio import AsyncIOMotorDatabase


async def db_create_user(
    user: user_schemas.UserCreate,
    db: AsyncIOMotorDatabase
# ) -> user_schemas.User:
):

    new_user = UserModel(**user.model_dump())
    await db['Users'].insert_one(new_user.model_dump())
    created_user = await db['Users'].find_one({'id': new_user.id})
    # print(created_user)
    return created_user
