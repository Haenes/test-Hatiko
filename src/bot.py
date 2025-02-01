import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from aiogram_dialog import setup_dialogs

from aiohttp import ClientSession
from redis.asyncio import Redis
from db.engine import async_session_maker

from dialog.dialogs import start, auth, login, register, imei
from middlewares.whitelist import WhiteListMiddleware
from commands import router
from settings import Settings


async def main():
    BOT_TOKEN = Settings.BOT_TOKEN
    API_BASE_URL = Settings.API_BASE_URL

    logging.basicConfig(level=logging.INFO)

    redis = Redis(host="redis", decode_responses=True)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=RedisStorage(
        redis,
        DefaultKeyBuilder(with_destiny=True)
    ))
    dp.update.outer_middleware(WhiteListMiddleware())

    dp.include_routers(router, start, auth, login, register, imei)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        db_sessionmaker=async_session_maker,
        redis=redis,
        session=ClientSession(base_url=API_BASE_URL, trust_env=True)
    )


if __name__ == "__main__":
    asyncio.run(main())
