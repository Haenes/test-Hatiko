from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Start, Group
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format, Const

from .states import StartSG, AuthSG, LoginSG, RegisterSG, ImeiSG
from .handlers import handle_input, register_user, login_user, check_IMEI


start = Dialog(
    Window(Format("{start_data}"), state=StartSG.main),
)

auth = Dialog(
    Window(
        Const("Ваш выбор?"),
        Group(
            Start(
                text=Const("Вход"),
                id="login",
                state=LoginSG.password
            ),
            Start(
                text=Const("Регистрация"),
                id="register",
                state=RegisterSG.password
            ),
            width=2,
        ),
        state=AuthSG.main,
    ),
)

login = Dialog(
    Window(
        Const("Введите пароль:"),
        TextInput(id="password", on_success=handle_input),
        state=LoginSG.password,
    ),
    Window(
        Format("{error}", "error"),
        SwitchTo(
            text=Const("Попробовать ещё раз"),
            id="try_again_to_login",
            state=LoginSG.password,
            when="error"
        ),
        Const("Вы успешно вошли!", when="success"),
        state=LoginSG.result,
        getter=login_user,
    ),
)

register = Dialog(
    Window(
        Const("Введите пароль:"),
        TextInput(id="password", on_success=handle_input),
        state=RegisterSG.password,
    ),
    Window(
        Format("{error}", "error"),
        SwitchTo(
            text=Const("Попробовать ещё раз"),
            id="try_again_to_register",
            state=RegisterSG.password,
            when="error"
        ),
        Const("Вы успешно зарегистрировались!", when="success"),
        state=RegisterSG.result,
        getter=register_user,
    ),
)

imei = Dialog(
    Window(
        Const(
            """\
                Введите IMEI для проверки.
                \nПосле ввода, это сообщение останется,\
                \nвам нужно будет немного подождать:
            """
        ),
        TextInput(id="imei", on_success=handle_input),
        state=ImeiSG.input,
    ),
    Window(
        Format("{result}", "result"),
        Format("{error}", "error"),
        SwitchTo(
            text=Const("Попробовать ещё раз"),
            id="try_again_check_imei",
            state=ImeiSG.input,
        ),
        state=ImeiSG.result,
        getter=check_IMEI
    ),
)
