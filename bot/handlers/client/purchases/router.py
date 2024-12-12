from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from dishka import FromDishka

from database.models import UserModel
from database.repos.purchases import PurchasesRepo

router = Router(name=__file__)


@router.callback_query(F.data == "purchases")
async def purchases_handler(
    callback: CallbackQuery,
    user: UserModel,
    purchases_repo: FromDishka[PurchasesRepo],
) -> None:
    purchases = await purchases_repo.get_user_purchases(user.id)
    if purchases:
        purchases_list = "\n".join(
            [f"{product.name} x{purchase.quantity}" for product, purchase in purchases],
        )

        text = (
            "<b>Купленные товары</b> 🧺\n\n"
            f"{purchases_list}\n\n"
            "Чтобы их забрать, подойдите к <u>магазину</u> или в <u>Отделение А-337</u>"
        )

    else:
        text = "<b>Ваша корзина пуста</b>"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        ],
    )
    await callback.message.answer(text=text, reply_markup=keyboard)

    await callback.message.delete()
