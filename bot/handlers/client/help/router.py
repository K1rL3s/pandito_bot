from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode

from .dialogs import help_dialog
from .states import HelpStates

router = Router(name=__file__)
router.include_router(help_dialog)


@router.message(Command("help"))
async def help_message_handler(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        HelpStates.help,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
