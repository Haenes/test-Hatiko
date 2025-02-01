from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from aiogram_dialog import DialogManager, StartMode

from redis.asyncio import Redis

from dialog.states import StartSG, AuthSG, ImeiSG
from dialog.utils import get_token


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, dialog_manager: DialogManager):
    text = (
        """\
            Привет, {user}!
            \nБыстрое введение по работе со мной:
            \n1) Вход/регистрация происходят через команду /auth.
            \n2) Проверка EMEI доступна по команде /imei.
        """
    ).format(user=dialog_manager.event.from_user.first_name)

    await dialog_manager.start(StartSG.main, data=text, mode=StartMode.RESET_STACK)


@router.message(Command("auth"))
async def cmd_auth(
    message: Message,
    redis: Redis,
    dialog_manager: DialogManager
):
    if await get_token(redis, message.from_user.id):
        return await message.answer("Вы уже вошли.")
    await dialog_manager.start(AuthSG.main, mode=StartMode.RESET_STACK)


@router.message(Command("imei"))
async def cmd_imei(
    message: Message,
    redis: Redis,
    dialog_manager: DialogManager
):
    if await get_token(redis, message.from_user.id):
        return await dialog_manager.start(ImeiSG.input, mode=StartMode.RESET_STACK)
    await message.answer("Вы не вошли, используйте команду /auth.")
