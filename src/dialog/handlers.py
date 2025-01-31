from aiogram.types import Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput

from aiohttp import ClientSession
from redis import Redis

from dialog.api_client import get_token, register, check_imei
from dialog.utils import isValidIMEI


async def handle_input(
    message: Message,
    text: ManagedTextInput,
    manager: DialogManager,
    input: str
):
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    await manager.next()


async def register_user(
    dialog_manager: DialogManager,
    session: ClientSession,
    redis: Redis,
    **kwargs
):
    username = dialog_manager.event.from_user.id
    password = dialog_manager.find("password").get_value()

    token = await register(session, username, password)

    if isinstance(token, dict):
        return {
            "error": token["error"],
            "try_again": "Попробовать снова"
        }

    await redis.set(username, token)
    return {"success": "Успешная регистрация!"}


async def login_user(
    dialog_manager: DialogManager,
    session: ClientSession,
    redis: Redis,
    **kwargs
):
    username = dialog_manager.event.from_user.id
    password = dialog_manager.find("password").get_value()

    token = await get_token(session, username, password)

    if isinstance(token, dict):
        return {
            "error": token["detail"],
            "try_again": "Попробовать снова"
        }

    await redis.set(username, token)
    return {"success": "Успешный вход!"}


async def check_IMEI(
    dialog_manager: DialogManager,
    session: ClientSession,
    redis: Redis,
    **kwargs
):
    imei = dialog_manager.find("imei").get_value()
    if not isValidIMEI(int(imei)):
        return {"error": "Неверный IMEI."}

    token = await redis.get(dialog_manager.event.from_user.id)
    results = await check_imei(session, token, imei)

    if results["status"] == "successful":
        return {"result": results["properties"]}
    elif results["status"] == "unsuccessful":
        return {"error": "Возникла ошибка у стороннего сервиса!"}
    return {"error": "Возникла ошибка!"}
