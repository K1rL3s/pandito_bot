from aiogram import F, Router
from aiogram.filters import CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode

from bot.handlers.client.start.states import StartStates
from bot.stickers import PANDA_HELLO

router = Router(name=__file__)


@router.message(CommandStart(), ~MagicData(F.user.name))
async def start_handler(message: Message, dialog_manager: DialogManager) -> None:
    await message.answer_sticker(sticker=PANDA_HELLO)
    await dialog_manager.start(
        state=StartStates.name,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
