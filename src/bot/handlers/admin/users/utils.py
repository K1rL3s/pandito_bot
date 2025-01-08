from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format

from bot.handlers.admin.users.view.states import ViewUserStates
from database.models import UserModel

_UserIdNameText = Format(
    "<code>{view_user.id}</code> | <b>{view_user.name}</b> - {role}",
)


async def on_go_view_user(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserModel = dialog_manager.dialog_data["view_user"]
    await dialog_manager.start(state=ViewUserStates.one, data={"view_user": user})
