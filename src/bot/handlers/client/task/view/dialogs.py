from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Next
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_active_task
from .on_actions import on_answer, on_cancel_task
from .states import ViewTaskStates

# TODO убрать айди?
view_task_window = Window(
    Format("<tg-spoiler>ID: {task.id}</tg-spoiler>"),
    Format("Название: {task.title}"),
    Format("Награда: {task.reward} Пятаков\n"),
    Format("{task.description}"),
    Button(Const("✏️ Ввести ответ"), id="answer", on_click=on_answer),
    Button(Const("❌ Отменить"), id="cancel", on_click=Next()),
    GoToMenuButton(),
    getter=get_active_task,
    state=ViewTaskStates.task,
)


cancel_task_window = Window(
    Const("❓ Вы уверены, что хотите отменить текущее задание?"),
    Button(Const("✅ Подтвердить"), id="cancel", on_click=on_cancel_task),
    Back(Const("⏪ Назад")),
    GoToMenuButton(),
    state=ViewTaskStates.cancel,
)


view_task_dialog = Dialog(
    view_task_window,
    cancel_task_window,
    on_start=on_start_update_dialog_data,
)
