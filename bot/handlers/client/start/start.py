from aiogram import F, Router
from aiogram.filters import CommandStart, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bot.states import Registration
from bot.stickers import PANDA_HELLO

router = Router(name=__file__)


@router.message(CommandStart(), ~MagicData(F.user.name))
async def start_handler(message: Message, state: FSMContext) -> None:
    await message.answer_sticker(sticker=PANDA_HELLO)
    await message.answer(
        "Привет! 👋\n\n"
        "Меня зовут <b>Пандито!</b> 🐼\n"
        "Я буду хранить твои <u>Иткоины</u> и оповещать тебя о всех важных событиях, "
        "приуроченных Дню рождения Института информационных технологий!\n\n"
        "Чтобы зарегистрироваться, введи свою <b>фамилию</b> и <b>имя</b>\n<i>"
        "(Пример: Иванов Ваня)</i>",
    )
    await state.set_state(Registration.name)


@router.callback_query(F.data == "help")
async def help_callback_handler(callback: CallbackQuery) -> None:
    text = (
        "Если у вас возникли вопросы или сложности в функционале "
        "<b>Пандито</b> — пишите @whatochka"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        ],
    )
    await callback.message.answer(text=text, reply_markup=keyboard)

    await callback.message.delete()
