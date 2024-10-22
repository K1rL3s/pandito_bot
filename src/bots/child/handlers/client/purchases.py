from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from infrastructure.database.repos import Database

router = Router(name=__file__)


@router.callback_query(F.data == "purchases")
async def purchases_handler(callback: CallbackQuery, db: Database):
    await callback.answer()
    await callback.message.delete()
    user = await db.get_user(callback.from_user.id)
    purchases = await db.get_user_purchases(int(user["id"]))
    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        ],
    )
    if purchases:
        purchases_list = "\n".join(
            [
                f"{purchase['product_name']} x{purchase['quantity_purchased']}"
                for purchase in purchases
            ],
        )

        full_message = (
            "<b>Купленные товары</b> 🧺\n\n"
            f"{purchases_list}\n\n"
            "Чтобы их забрать, подойдите к <u>магазину</u>, либо в <u>Отделение А-337</u>"
        )

        await callback.message.answer(
            full_message,
            reply_markup=c_bk,
            parse_mode="HTML",
        )
    else:
        await callback.message.answer(
            "<b>Ваша корзина пуста</b>",
            reply_markup=c_bk,
            parse_mode="HTML",
        )
