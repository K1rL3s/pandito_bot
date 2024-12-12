from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from dishka import FromDishka

from core.services.broadcast import Broadcaster

router = Router(name=__file__)


@router.message(Command("broadcast"), StateFilter(None))
async def admin_broadcast(
    message: Message,
    command: CommandObject,
    bot: Bot,
    broadcaster: FromDishka[Broadcaster],
) -> None:
    if command.args:
        text = command.args
        result = await broadcaster.broadcast(bot, text)
        await message.answer(f"Успешный успех, ok={result.ok} fail={result.fail}")
    else:
        await message.answer("Формат: /broadcast <message>", parse_mode=None)
