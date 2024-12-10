from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from dishka import FromDishka

from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.message(Command("stage"), StateFilter(None))
async def admin_change_stage(
    message: Message,
    command: CommandObject,
    users_repo: FromDishka[UsersRepo],
) -> None:
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        user_id, stage = int(args[0]), int(args[1])
        await users_repo.change_stage(user_id, stage)
        await message.answer("Успех!")
    else:
        await message.answer("Формат: /stage <user_id> <stage>", parse_mode=None)


@router.message(Command("list_users"), StateFilter(None))
async def list_users(
    message: Message,
    users_repo: FromDishka[UsersRepo],
) -> None:
    users = await users_repo.get_all()
    if users:
        user_list = "\n".join(
            [
                f"ID: {user.id}, ФИО: {user.name}, Баланс: {user.balance} Ит."
                for user in users
            ],
        )
        await message.answer(f"<b>Список участников:</b>\n\n{user_list}")
    else:
        await message.answer("Нет зарегистрированных участников.")
