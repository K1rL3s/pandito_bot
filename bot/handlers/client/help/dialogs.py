from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.dialogs.on_actions import on_go_to_menu

from .states import HelpStates

help_dialog = Dialog(
    Window(
        Const(
            "Если у вас возникли вопросы или сложности в функционале <b>Пандито</b> — пишите @whatochka",  # noqa: E501
        ),
        Button(Const("🔙 В меню 🔙"), id="to_menu", on_click=on_go_to_menu),
        state=HelpStates.help,
    ),
)
