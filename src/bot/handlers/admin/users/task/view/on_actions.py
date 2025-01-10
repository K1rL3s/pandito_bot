from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from core.ids import UserId

from ..cancel.states import CancelTaskStates
from ..confirm.states import ConfirmTaskStates


async def on_confirm_task(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(
        ConfirmTaskStates.confirm,
        data={"view_user_id": user_id},
    )


async def on_cancel_task(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(
        CancelTaskStates.cancel,
        data={"view_user_id": user_id},
    )
