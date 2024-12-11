import contextlib
import re

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from dishka import FromDishka

from bot.states import TransferFunds
from core.services.users import UsersService
from database.models import UserModel
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.callback_query(F.data == "transfer_funds")
async def transfer_funds_handler(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Введите id человека, которому хотите перевести <b>Иткоины</b>"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]],
    )

    await callback.message.answer(text=text, reply_markup=keyboard)

    await state.set_state(TransferFunds.receiver_id)
    await callback.message.delete()


@router.message(TransferFunds.receiver_id)
async def transfer_funds_id_handler(
    message: Message,
    state: FSMContext,
    users_repo: FromDishka[UsersRepo],
) -> None:
    receiver_id = message.text.strip()
    if not re.match(r"^\d+$", receiver_id):
        await message.answer("Неверный формат!")
        return

    receiver = await users_repo.get_by_id(int(receiver_id))
    if not receiver:
        text = f"Пользователя с id {receiver_id} не существует!"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
            ],
        )
        await message.answer(text=text, reply_markup=keyboard)
        return

    text = (
        f"Перевод будет произведен пользователю с именем <b>{receiver.name}</b>\n\n"
        f"Если всё верно введите сумму перевода"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]],
    )
    await message.answer(text=text, reply_markup=keyboard)

    await state.update_data(receiver_id=int(receiver_id))
    await state.set_state(TransferFunds.amount)


@router.message(TransferFunds.amount)
async def transfer_funds_amount_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    user: UserModel,
    users_service: FromDishka[UsersService],
) -> None:
    amount = message.text.strip()
    if not re.match(r"^\d+$", amount) or int(amount) <= 0:
        await message.answer("Неверный формат!")
        return
    amount = int(amount)

    if user.balance < amount:
        text = "У вас недостаточно для перевода, введите другую сумму"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
            ],
        )
        await message.answer(text=text, reply_markup=keyboard)
        return

    data = await state.get_data()
    receiver_id = int(data["receiver_id"])

    await users_service.transfer_funds(user.id, receiver_id, int(amount))

    with contextlib.suppress(TelegramAPIError):  # TODO сделать норм
        await bot.send_message(
            chat_id=receiver_id,
            text=f"Вам перевели {amount} Ит.!",
        )

    text = "Операция прошла успешно!"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Главное меню", callback_data="cancel")],
        ],
    )
    await message.answer(text=text, reply_markup=keyboard)

    await state.clear()
