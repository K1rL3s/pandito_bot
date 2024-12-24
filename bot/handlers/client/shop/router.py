from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.enums import SlashCommand
from bot.handlers.client.shop.states import ShopStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.SHOP))
async def open_shop_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=ShopStates.list,
    )
