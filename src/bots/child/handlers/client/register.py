import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from bots.child.states import Registration
from infrastructure.database.repos import Database

router = Router(name=__file__)


@router.message(Registration.name)
async def register_name_handler(message: Message, state: FSMContext):
    full_name = message.text.strip()
    if not re.match(r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$", full_name):
        await message.answer("Неверный формат!")
        return

    await state.update_data(full_name=full_name)
    confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подтвердить", callback_data="yes"),
                InlineKeyboardButton(text="Отмена", callback_data="no"),
            ],
        ],
    )
    await message.answer(
        f"Проверьте введенные данные!\n\nВас зовут <b>{full_name}</b>?",
        reply_markup=confirm_kb,
        parse_mode="HTML",
    )
    await state.set_state(Registration.confirm)
    await state.update_data(name=full_name)


@router.callback_query(Registration.confirm, F.data == "yes")
async def register_confirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
    db: Database,
    owner_id: int,
):
    await callback.answer()
    state_data = await state.get_data()
    user_id = await db.create_user(
        callback.from_user.id,
        state_data["name"],
        callback.from_user.id == owner_id,
    )
    kb = [[KeyboardButton(text="/menu")]]
    kb_menu = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await callback.message.delete()

    await callback.message.answer_sticker(
        r"CAACAgIAAxkBAAEM7dhnAxdZxlqB__bt8a5GR5wo9-vxJAACDQADWbv8JS5RHx3i_HUDNgQ",
    )
    await callback.message.answer(
        f"Вы успешно зарегистрировались! 🎉\n\n<b>Ваш id: {user_id}</b>\n\n"
        f"Теперь вы можете вызывать <b>меню</b> командой <i>/menu</i>",
        reply_markup=kb_menu,
        parse_mode="HTML",
    )
    await state.clear()


@router.callback_query(Registration.confirm, F.data == "no")
async def register_disconfirm_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_data({})
    await callback.message.answer("Бывает, попробуй еще раз!")
    await state.set_state(Registration.name)
    await callback.message.delete()
