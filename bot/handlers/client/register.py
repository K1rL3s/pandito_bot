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
from dishka import FromDishka

from bot.states import Registration
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.message(Registration.name, F.text)
async def register_name_handler(message: Message, state: FSMContext) -> None:
    full_name = message.text.strip()
    if not re.match(r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$", full_name):
        await message.answer("Неверный формат!")
        return

    text = f"Проверьте введенные данные!\n\nВас зовут <b>{full_name}</b>?"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подтвердить", callback_data="yes"),
                InlineKeyboardButton(text="Отмена", callback_data="no"),
            ],
        ],
    )
    await message.answer(text=text, reply_markup=keyboard)

    await state.set_state(Registration.confirm)
    await state.update_data(full_name=full_name)


@router.callback_query(Registration.confirm, F.data == "yes")
async def register_confirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
    owner_id: int,
    users_repo: FromDishka[UsersRepo],
) -> None:
    state_data = await state.get_data()
    user_id = callback.from_user.id

    await users_repo.update(user_id, state_data["full_name"], user_id == owner_id)

    text = (
        f"Вы успешно зарегистрировались! 🎉\n\n<b>Ваш id: {user_id}</b>\n\n"
        "Теперь вы можете вызывать <b>меню</b> командой <i>/menu</i>"
    )
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/menu")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await callback.message.answer_sticker(
        r"CAACAgIAAxkBAAEM7dhnAxdZxlqB__bt8a5GR5wo9-vxJAACDQADWbv8JS5RHx3i_HUDNgQ",
    )
    await callback.message.answer(text=text, reply_markup=keyboard)
    await callback.message.delete()
    await state.clear()


@router.callback_query(Registration.confirm, F.data == "no")
async def register_disconfirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.answer("Бывает, попробуй еще раз!")
    await callback.message.delete()
    await state.set_data({})
    await state.set_state(Registration.name)
