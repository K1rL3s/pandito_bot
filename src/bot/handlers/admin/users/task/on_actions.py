from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from core.ids import UserId

from .view.states import TaskUserStates


async def on_go_user_task(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(TaskUserStates.task, data={"view_user_id": user_id})
