from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ...on_actions import on_go_view_user
from ..on_actions import on_go_user_task
from .states import ConfirmTaskStates

# TODO: подтверждение задания
confirm_task_window = Window(
    Const("Уверены, что хотите засчитать выполнение задания?"),
    Button(Const("✅ Подтвердить"), id="confirm", on_click=None),
    Button(Const("⏪ Задание"), id="task", on_click=on_go_user_task),
    Button(Const("⏪ Юзер"), id="user", on_click=on_go_view_user),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    state=ConfirmTaskStates.confirm,
)

confirm_task_dialog = Dialog(confirm_task_window, on_start=on_start_update_dialog_data)