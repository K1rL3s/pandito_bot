from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.enums import SlashCommand

from .states import HelpStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.HELP))
async def help_message_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=HelpStates.help)
