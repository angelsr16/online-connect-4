from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from api.dependencies.db import get_database
from core import config
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.crud import user as crud_user
from db.helpers.user import user_helper


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def verify_token(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> str:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        user = await crud_user.get_user_by_username(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user_helper(user)
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")
