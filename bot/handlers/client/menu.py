from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dishka import FromDishka

from bot.keyboards.menu import generate_main_menu
from bot.stickers import PANDA_WINK
from bot.utils.menu_text import menu_text
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.message(Command("menu", "profile", "balance"))
async def menu_handler(
    message: Message,
    state: FSMContext,
    users_repo: FromDishka[UsersRepo],
) -> None:
    await message.answer_sticker(sticker=PANDA_WINK)

    user = await users_repo.get_by_id(message.from_user.id)
    text = menu_text(user.id, user.balance, user.stage, user.is_admin)
    keyboard = await generate_main_menu(user, users_repo)
    await message.answer(text=text, reply_markup=keyboard)

    await message.delete()
    await state.clear()
