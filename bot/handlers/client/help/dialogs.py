from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

from bot.dialogs.buttons import GoToMenuButton

from .states import HelpStates

help_dialog = Dialog(
    Window(
        Const(
            "Если у вас возникли вопросы или сложности в функционале <b>Пандито</b> — пишите @whatochka",  # noqa: E501
        ),
        GoToMenuButton(),
        state=HelpStates.help,
    ),
)
