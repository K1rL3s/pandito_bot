from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka

from bot.keyboards.menu import generate_main_menu
from bot.utils.menu_text import menu_text
from database.models import UserModel
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.callback_query(F.data == "cancel")
async def cancel_handler(
    callback: CallbackQuery,
    state: FSMContext,
    user: UserModel,
    users_repo: FromDishka[UsersRepo],
) -> None:
    text = menu_text(user.id, user.balance, user.stage, user.is_admin)
    keyboard = await generate_main_menu(user, users_repo)
    await callback.message.answer(text=text, reply_markup=keyboard)
    await callback.message.delete()

    await state.clear()
