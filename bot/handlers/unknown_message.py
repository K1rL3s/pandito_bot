from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router(name=__file__)


@router.message(StateFilter(None))
async def unknown_msg(message: Message) -> None:
    await message.delete()
