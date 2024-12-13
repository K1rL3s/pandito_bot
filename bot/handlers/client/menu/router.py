from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode

from bot.stickers import PANDA_WINK
from database.models import UserModel

from .states import MenuState

router = Router(name=__file__)


@router.message(Command("menu", "profile", "balance", "me"))
async def menu_handler(
    message: Message,
    user: UserModel,
    dialog_manager: DialogManager,
) -> None:
    await message.answer_sticker(sticker=PANDA_WINK)
    await dialog_manager.start(
        state=MenuState.menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={"role": user.role},
    )
