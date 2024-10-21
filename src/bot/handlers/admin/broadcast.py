from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message

from database.database import Database

router = Router(name=__file__)


@router.message(Command("broadcast"), StateFilter(None))
async def admin_broadcast(
    message: Message,
    command: CommandObject,
    bot: Bot,
    db: Database,
):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args:
        text = command.args
        users = await db.get_all_users()
        for user in users:
            await bot.send_message(user["tg"], text)
        await message.answer("Успешный успех")
    else:
        await message.answer("Формат: /broadcast <message>")
