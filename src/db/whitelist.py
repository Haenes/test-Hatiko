from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base


class Whitelist(Base):
    __tablename__ = "test_whitelist"

    user_id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False
    )


async def is_in_whitelist(user_id: int, session: AsyncSession) -> bool:
    query = select(Whitelist.user_id).where(Whitelist.user_id == user_id)
    result = await session.scalar(query)

    if result is None:
        return False
    return True
