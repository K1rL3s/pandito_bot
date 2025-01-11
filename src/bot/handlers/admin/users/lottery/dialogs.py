from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToUserButton
from ..getters import user_short_link
from .on_actions import group_input_handler, student_id_input_handler
from .states import LotteryUserStates

set_student_window = Window(
    Const("🆔 Введите номер студенческого"),
    Format("Текущий: {view_user.student_id}"),
    MessageInput(
        student_id_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    GoToUserButton,
    GoToAdminPanelButton(),
    GoToMenuButton(),
    state=LotteryUserStates.student_id,
    getter=user_short_link,
)

set_group_window = Window(
    Const("🎓 Введите группу студента"),
    Format("Текущая: {view_user.group}"),
    MessageInput(
        group_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    state=LotteryUserStates.group,
    getter=user_short_link,
)

set_lottery_info_dialog = Dialog(
    set_student_window,
    set_group_window,
    on_start=on_start_update_dialog_data,
)
