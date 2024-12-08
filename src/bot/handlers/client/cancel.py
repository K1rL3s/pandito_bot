from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.menu import generate_main_menu
from bot.utils.menu_text import menu_text
from database.repos.database import Database

router = Router(name=__file__)


@router.callback_query(F.data == "cancel")
async def cancel_handler(callback: CallbackQuery, state: FSMContext, db: Database):
    await state.clear()
    user = await db.get_user(callback.from_user.id)
    menu_kb = await generate_main_menu(user, db)

    await callback.message.answer(
        text=menu_text(user["id"], user["balance"], user["stage"], user["is_admin"]),
        reply_markup=menu_kb,
        parse_mode="HTML",
    )
    await callback.message.delete()
