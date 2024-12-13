from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode

from bot.callbacks.universal import OpenWindow
from bot.enums import BotWindow

from .states import HelpStates

router = Router(name=__file__)


@router.message(Command("help"))
async def help_message_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        HelpStates.help,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


@router.callback_query(OpenWindow.filter(F.window == BotWindow.HELP))
async def help_callback_handler(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        HelpStates.help,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
