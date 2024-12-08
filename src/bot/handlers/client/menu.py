from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.menu import generate_main_menu
from bot.utils.menu_text import menu_text
from database.repos.database import Database

router = Router(name=__file__)


@router.message(Command("menu"))
async def menu_handler(message: Message, state: FSMContext, db: Database):
    await state.clear()
    await message.answer_sticker(
        r"CAACAgIAAxkBAAEM7eFnAzNGgGnjM59XOgjO_cpmrvdFhAACFwADWbv8Jfuhn7EBJTs2NgQ",
    )
    user = await db.get_user(message.from_user.id)
    menu_kb = await generate_main_menu(user, db)

    await message.answer(
        text=menu_text(user["id"], user["balance"], user["stage"], user["is_admin"]),
        reply_markup=menu_kb,
    )
    await message.delete()
