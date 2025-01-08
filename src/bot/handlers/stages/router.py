import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from dishka import FromDishka

from bot.states import StartStage
from core.services.users import UsersService
from database.models import UserModel
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.callback_query(F.data == "start_stage")
async def start_stage_handler(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Введите id участника, который пришел на этап:"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]],
    )
    await callback.message.answer(text=text, reply_markup=keyboard)
    await callback.message.delete()

    await state.set_state(StartStage.participant_id)


@router.message(StartStage.participant_id)
async def stage_participant_id_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    users_repo: FromDishka[UsersRepo],
) -> None:
    participant_id = message.text.strip()
    if not re.match(r"^\d+$", participant_id):
        await message.answer("Неверный формат id! Попробуйте еще раз.")
        return

    # Проверяем, существует ли пользователь с таким id
    slave = await users_repo.get_by_id(int(participant_id))
    if not slave:
        await message.answer("Такого участника не существует.")
        return

    await state.update_data(participant_id=participant_id)

    if user.stage == 1:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="10", callback_data="reward_10")],
                [InlineKeyboardButton(text="20", callback_data="reward_20")],
                [InlineKeyboardButton(text="30", callback_data="reward_30")],
            ],
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="10", callback_data="reward_10")],
            ],
        )

    await message.answer("Выберите сумму для начисления:", reply_markup=keyboard)
    await state.set_state(StartStage.reward_amount)


@router.callback_query(StartStage.reward_amount, F.data.startswith("reward_"))
async def stage_reward_handler(
    callback: CallbackQuery,
    state: FSMContext,
    user: UserModel,
    users_service: FromDishka[UsersService],
) -> None:
    data = await state.get_data()

    amount = int(callback.data.split("_")[1])
    participant_id = int(data["participant_id"])

    await users_service.admin_update_balance(participant_id, user.id, amount)

    text = f"Участнику с id {participant_id} начислено {amount} Пятаков"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪ Назад ⏪", callback_data="start_stage")],
        ],
    )

    await callback.message.answer(text=text, reply_markup=keyboard)

    await callback.message.delete()
    await state.clear()
