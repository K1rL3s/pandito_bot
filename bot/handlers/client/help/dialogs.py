from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .states import HelpStates

help_dialog = Dialog(
    Window(
        Const(
            "Если у вас возникли вопросы или сложности в функционале <b>Пандито</b> — пишите @whatochka",  # noqa: E501
        ),
        Button(Const("🔙 Назад 🔙"), id="to_menu"),
        state=HelpStates.help,
    ),
)
