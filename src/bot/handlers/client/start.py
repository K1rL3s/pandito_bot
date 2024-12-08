from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bot.states import Registration
from database.repos.database import Database

router = Router(name=__file__)


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, db: Database):
    user = await db.get_user(message.from_user.id)
    if user:
        return

    await message.answer_sticker(
        r"CAACAgIAAxkBAAEM7c9nAwuUZBCLVlLpmPHfk4bNQcpXOwACHwADWbv8Jeo5dBvZPTaZNgQ",
    )
    await message.answer(
        "Привет! 👋\n\n"
        "Меня зовут <b>Пандито!</b> 🐼\n"
        "Я буду хранить твои <u>Иткоины</u> и оповещать тебя о всех важных событиях, "
        "приуроченных Дню рождения Института информационных технологий!\n\n"
        "Чтобы зарегистрироваться введи свою <b>фамилию</b> и <b>имя</b>\n<i>"
        "(Пример: Иванов Ваня)</i>",
        parse_mode="HTML",
    )
    await state.set_state(Registration.name)


@router.callback_query(F.data == "help")
async def help_callback_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        ],
    )

    await callback.message.answer(
        "Если у вас возникли вопросы или сложности в функционале <b>Пандито</b> "
        "— пишите @whatochka",
        reply_markup=c_bk,
        parse_mode="HTML",
    )
