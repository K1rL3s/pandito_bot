from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.enums import SlashCommand
from bot.handlers.admin.secrets.view.states import ViewSecretsStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.SECRETS))
async def list_secrets_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=ViewSecretsStates.list)
