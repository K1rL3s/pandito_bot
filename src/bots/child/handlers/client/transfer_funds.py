import re

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bots.child.states import TransferFunds
from infrastructure.database.repos import Database

router = Router(name=__file__)


@router.callback_query(F.data == "transfer_funds")
async def transfer_funds_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()
    await state.set_state(TransferFunds.receiver_id)
    ckb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]],
    )
    await callback.message.answer(
        "Введите id человека, которому хотите перевести <b>Иткоины</b>",
        reply_markup=ckb,
        parse_mode="HTML",
    )


@router.message(TransferFunds.receiver_id)
async def transfer_funds_id_handler(message: Message, state: FSMContext, db: Database):
    id = message.text.strip()
    if not re.match(r"^\d+$", id):
        await message.answer("Неверный формат!")
        return
    receiver = await db.get_user_by_id(int(id))
    if not receiver:
        ckb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
            ],
        )
        await message.answer(f"Пользователя с id {id} не существует!", reply_markup=ckb)
        return
    ckb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]],
    )
    await state.update_data(receiver_id=id, receiver_tg=receiver["tg"])
    await state.set_state(TransferFunds.amount)
    await message.answer(
        f"Перевод будет произведен пользователю с именем <b>{receiver['name']}</b>\n\n"
        f"Если всё верно введите сумму перевода",
        reply_markup=ckb,
        parse_mode="HTML",
    )


@router.message(TransferFunds.amount)
async def transfer_funds_amount_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    db: Database,
):
    amount = message.text.strip()
    if not re.match(r"^\d+$", amount) or int(amount) == 0:
        await message.answer("Неверный формат!")
        return
    user = await db.get_user(message.from_user.id)
    ckb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]],
    )
    scb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Главное меню", callback_data="cancel")],
        ],
    )
    if user["balance"] < int(amount):
        await message.answer(
            "У вас недостаточно для перевода, введите другую сумму",
            reply_markup=ckb,
        )
    data = await state.get_data()
    await db.transfer_funds(int(user["id"]), int(data["receiver_id"]), int(amount))
    await message.answer("Операция прошла успешно!", reply_markup=scb)
    await bot.send_message(
        data["receiver_tg"],
        f"Вам перевели {amount.lstrip('0')} Ит.!",
    )
    await state.clear()
