from sqlalchemy import VARCHAR
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base


class User(Base):
    __tablename__ = "test_user"

    user_id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        VARCHAR(128),
        nullable=False
    )

    def __str__(self):
        return f"User({self.user_id}, {self.hashed_password})"


async def create_user(user: User, session: AsyncSession) -> int | None:
    try:
        await session.merge(user)
        await session.commit()
    except Exception:
        return None


async def get_user(user_id: int, session: AsyncSession) -> User | None:
    query = select(User).where(User.user_id == user_id)
    return await session.scalar(query)
