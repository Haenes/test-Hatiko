from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db.whitelist import is_in_whitelist


class WhiteListMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        db_sessionmaker = data["db_sessionmaker"]
        user_id = data["event_from_user"].id

        async with db_sessionmaker() as session:
            is_allowed = await is_in_whitelist(user_id, session)

        if is_allowed:
            return await handler(event, data)
        print("User not in the whitelist.")
