from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.handlers.admin.broadcast.states import BroadcastStates
from bot.handlers.admin.secret.states import ViewSecretsStates


async def on_go_to_broadcast(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=BroadcastStates.wait)


async def on_go_to_secrets(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=ViewSecretsStates.list)
