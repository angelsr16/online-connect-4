from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.dependencies.db import get_database
from db.crud import user as crud_user

from db.models.user import UserCreate, UserInDB
from services.auth import authenticate_user, get_password_hash
from services.jwt import create_access_token

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register_user(
    user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)
):
    find_user = await crud_user.get_user_by_username(db, user.username)

    if find_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered!"
        )

    hashed_pw = get_password_hash(user.password)

    user_db = UserInDB(
        username=user.username,
        hashed_password=hashed_pw,
    )

    await crud_user.create_user(db, user_db.model_dump(by_alias=True, exclude={"id"}))
    access_token = create_access_token(data={"sub": user_db.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user_db.username,
    }


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": user["username"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user["username"],
    }
