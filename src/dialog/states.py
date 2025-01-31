from aiogram.filters.state import State, StatesGroup


class StartSG(StatesGroup):
    main = State()


class AuthSG(StatesGroup):
    main = State()


class RegisterSG(StatesGroup):
    password = State()
    result = State()


class LoginSG(StatesGroup):
    password = State()
    result = State()


class ImeiSG(StatesGroup):
    input = State()
    result = State()
