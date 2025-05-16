from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.crud import user as crud_user
from db.models.user import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(
    db: AsyncIOMotorDatabase, username: str, password: str
) -> dict:
    user_doc = await crud_user.get_user_by_username(db, username)

    if not user_doc:
        return None

    user = UserInDB(**user_doc)

    if not verify_password(password, user.hashed_password):
        return None

    return user.model_dump(exclude={"hashed_password"})
