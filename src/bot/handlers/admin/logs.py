from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message

from database.repos.database import Database

router = Router(name=__file__)


@router.message(Command("logs"), StateFilter(None))
async def admin_view_logs(message: Message, command: CommandObject, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args and len(command.args.split()) == 1:
        user_id = int(command.args.strip())
        logs = await db.get_user_logs(user_id)
        log_texts = [f"{log['created_at']}: {log['description']}" for log in logs][:10]
        await message.answer("\n".join(log_texts) or "Нет логов")
    else:
        await message.answer("Формат: /logs <user_id>")
