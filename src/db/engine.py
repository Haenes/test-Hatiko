import os
from typing import AsyncGenerator
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)


load_dotenv()

engine = create_async_engine(url=os.environ.get("DB_URI"), echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
