from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message

from infrastructure.database.repos import Database

router = Router(name=__file__)


@router.message(Command("money"), StateFilter(None))
async def admin_add_money(message: Message, command: CommandObject, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        user_id, amount = int(args[0]), int(args[1])
        await db.update_user_balance(user_id, amount, user["id"])
        await message.answer(f"Добавлено {amount} пользователю {user_id}")
    else:
        await message.answer("Формат: /money <user_id> <amount>")
