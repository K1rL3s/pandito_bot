from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Group
from aiogram_dialog.widgets.text import Const

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import user_short_link
from ..utils import _UserIdNameText
from .on_actions import id_input_handler, on_check_cart, on_set_role
from .states import ViewUserStates

wait_user_id_window = Window(
    Const("Введите ID человека, которого хотите увидеть"),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    MessageInput(
        id_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    state=ViewUserStates.id,
)

view_user_window = Window(
    _UserIdNameText,
    Group(
        Button(Const("🧺 Корзина"), id="cart", on_click=on_check_cart),
        Button(Const("💼 Задание"), id="task", on_click=None),
        Button(Const("👨‍💼 Выдать роль"), id="role", on_click=on_set_role),
        width=2,
    ),
    Back(Const("🔁 Ввести ID")),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=user_short_link,
    state=ViewUserStates.one,
)

view_user_dialog = Dialog(
    wait_user_id_window,
    view_user_window,
    on_start=on_start_update_dialog_data,
)
