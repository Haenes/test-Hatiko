from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.models import Token
from backend.auth.jwt_bearer import (
    hash_password,
    authenticate_user,
    create_access_token
)
from backend.redis import get_redis_client
from db.engine import get_async_session
from db.user import User, create_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    redis: Annotated[Redis, Depends(get_redis_client)],
) -> Token:
    user = User(
        user_id=int(form_data.username),
        hashed_password=hash_password(form_data.password)
    )
    await create_user(user, session)

    access_token = create_access_token({"sub": str(form_data.username)})

    await redis.set(user.user_id, access_token)
    return Token(access_token=access_token, token_type="Bearer")


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    redis: Annotated[Redis, Depends(get_redis_client)],
) -> Token:
    user = await authenticate_user(
        session,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Неверный юзернейм или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": str(user.user_id)})

    await redis.set(user.user_id, access_token)
    return Token(access_token=access_token, token_type="Bearer")
