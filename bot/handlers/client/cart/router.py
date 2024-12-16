from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode

from bot.enums import SlashCommand
from bot.handlers.client.cart.states import CartStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.CART))
async def cart_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=CartStates.cart,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
