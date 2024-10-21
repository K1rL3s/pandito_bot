import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bot.states import StartStage
from database.database import Database

router = Router(name=__file__)


@router.callback_query(F.data == "start_stage")
async def start_stage_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StartStage.participant_id)
    await callback.message.delete()
    ckb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]],
    )
    await callback.message.answer(
        "Введите id участника, который пришел на этап:",
        reply_markup=ckb,
    )


@router.message(StartStage.participant_id)
async def stage_participant_id_handler(
    message: Message,
    state: FSMContext,
    db: Database,
):
    participant_id = message.text.strip()
    if not re.match(r"^\d+$", participant_id):
        await message.answer("Неверный формат id! Попробуйте еще раз.")
        return

    # Проверяем, существует ли пользователь с таким id
    user_id = await db.get_user_by_id(int(participant_id))
    user = await db.get_user(message.from_user.id)
    if not user_id:
        await message.answer("Такого участника не существует.")
        return

    await state.update_data(participant_id=participant_id)

    if user["stage"] == 1:
        ckb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="10", callback_data="reward_10")],
                [InlineKeyboardButton(text="20", callback_data="reward_20")],
                [InlineKeyboardButton(text="30", callback_data="reward_30")],
            ],
        )
    else:
        ckb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="10", callback_data="reward_10")],
            ],
        )
    await state.set_state(StartStage.reward_amount)
    await message.answer("Выберите сумму для начисления:", reply_markup=ckb)


@router.callback_query(StartStage.reward_amount, F.data.startswith("reward_"))
async def stage_reward_handler(
    callback: CallbackQuery,
    state: FSMContext,
    db: Database,
):
    await callback.answer()
    await callback.message.delete()
    amount = int(
        callback.data.split("_")[1],
    )  # Получаем число из callback_data (10, 20, 30)
    data = await state.get_data()
    user = await db.get_user(callback.from_user.id)
    participant_id = int(data["participant_id"])

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="start_stage")],
        ],
    )

    # Начисляем валюту
    await db.update_user_balance(participant_id, amount, user["id"])

    await callback.message.answer(
        f"Участнику с id {participant_id} начислено {amount} Ит.",
        reply_markup=c_bk,
    )
    await state.clear()
