from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from dishka import FromDishka

from database.repos.users import UsersRepo


router = Router(name=__file__)


@router.message(Command("broadcast"), StateFilter(None))
async def admin_broadcast(
    message: Message,
    command: CommandObject,
    bot: Bot,
    users_repo: FromDishka[UsersRepo],
) -> None:
    if command.args:
        text = command.args
        users = await users_repo.get_all_users()
        for user in users:
            await bot.send_message(user.id, text)  # TODO нормальная рассылка
        await message.answer("Успешный успех")
    else:
        await message.answer("Формат: /broadcast <message>")
