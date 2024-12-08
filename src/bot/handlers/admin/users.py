from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message

from database.repos.database import Database

router = Router(name=__file__)


@router.message(Command("stage"), StateFilter(None))
async def admin_change_stage(message: Message, command: CommandObject, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        user_id, stage = int(args[0]), int(args[1])
        await db.change_stage(user_id, stage)
        await message.answer("Успех!")
    else:
        await message.answer("Формат: /stage <user_id> <stage>")


@router.message(Command(commands=["list_users"]))
async def list_users(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    users = await db.get_all_users()
    if users:
        user_list = "\n".join(
            [
                f"ID: {user['id']}, ФИО: {user['name']}, Баланс: {user['balance']} Ит."
                for user in users
            ],
        )
        await message.answer(
            f"<b>Список участников:</b>\n\n{user_list}",
            parse_mode="HTML",
        )
    else:
        await message.answer("Нет зарегистрированных участников.")
