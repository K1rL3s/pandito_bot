from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import UserModel
from database.repos.users import UsersRepo


async def generate_main_menu(
    user: UserModel,
    users_repo: UsersRepo,
) -> InlineKeyboardMarkup:
    if user.stage == 0:  # участник
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Магазин 🛍️",
                        callback_data="view_products",
                    ),
                    InlineKeyboardButton(text="Корзина 🧺", callback_data="purchases"),
                ],
                [
                    InlineKeyboardButton(
                        text="Перевод 💸",
                        callback_data="transfer_funds",
                    ),
                    InlineKeyboardButton(text="Помощь 🆘", callback_data="help"),
                ],
            ],
        )
    if user.stage == 1:  # этапщик
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Начать этап",
                        callback_data="start_stage",
                    ),
                    InlineKeyboardButton(text="Помощь", callback_data="help"),
                ],
            ],
        )
    if user.stage == 2:  # продавец
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Магазин продавца",
                        callback_data="view_products_salesman",
                    ),
                    InlineKeyboardButton(
                        text="Корзина участника",
                        callback_data="members_purchases",
                    ),
                ],
                [InlineKeyboardButton(text="Помощь", callback_data="help")],
            ],
        )
    if user.stage == 3:  # RTUITLab
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Начать этап",
                        callback_data="start_stage",
                    ),
                    InlineKeyboardButton(text="Помощь", callback_data="help"),
                ],
            ],
        )

    await users_repo.change_stage(user.id, 0)

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Магазин 🛍️",
                    callback_data="view_products",
                ),
                InlineKeyboardButton(text="Корзина 🧺", callback_data="purchases"),
            ],
            [
                InlineKeyboardButton(
                    text="Перевод 💸",
                    callback_data="transfer_funds",
                ),
                InlineKeyboardButton(text="Помощь 🆘", callback_data="help"),
            ],
        ],
    )
