from datetime import datetime, timedelta
from jose import JWTError, jwt
from core import config


def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


