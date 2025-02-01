from os import environ
from dotenv import load_dotenv
from typing import Annotated, NoReturn

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.models import TokenData
from db.engine import get_async_session
from db.user import User, get_user


load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


SECRET = environ.get("JWT_SECRET")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str
) -> User | None:
    user = await get_user(int(username), session)

    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET, ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> User | NoReturn:
    error_401 = HTTPException(
        status_code=401,
        detail="Ошибка валидации данных",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET, [ALGORITHM], {"verify_exp": False})
        username = int(payload.get("sub"))

        if username is None:
            raise error_401
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise error_401

    user = await get_user(token_data.username, session)

    if user is None:
        raise error_401
    return user
