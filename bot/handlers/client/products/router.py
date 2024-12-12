from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from dishka import FromDishka

from bot.callbacks.products import BuyProductCallback, ViewProductCallback
from bot.keyboards.products import (
    buy_product_keyboard,
    products_keyboard,
    view_shop_keyboard,
)
from core.services.products import ProductsService
from database.models import UserModel
from database.repos.products import ProductsRepo

router = Router(name=__file__)


@router.callback_query(F.data == "view_products")
async def view_products_handler(
    callback: CallbackQuery,
    user: UserModel,
    products_repo: FromDishka[ProductsRepo],
) -> None:
    products = await products_repo.get_available()

    if not products:
        await callback.message.answer(
            "Упс, сейчас ничего в наличии нет",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
                ],
            ),
        )
        await callback.message.delete()
        return

    text = f"Список товаров 🛍️\n\nБаланс: {user.balance} Ит."
    keyboard = products_keyboard(products)
    await callback.message.answer(text=text, reply_markup=keyboard)

    await callback.message.delete()


@router.callback_query(ViewProductCallback.filter())
async def view_one_product_handler(
    callback: CallbackQuery,
    callback_data: ViewProductCallback,
    products_repo: FromDishka[ProductsRepo],
) -> None:
    product = await products_repo.get_one(callback_data.id)
    if not product:
        return

    if product.stock > 0:
        text = f"{product.id}. <b>{product.name}</b>\n\n{product.description}"
        keyboard = buy_product_keyboard(product)
    else:
        text = "Упс, уже раскупили"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔙 Назад 🔙",
                        callback_data="view_products",
                    ),
                ],
            ],
        )

    await callback.message.answer(text=text, reply_markup=keyboard)
    await callback.message.delete()


@router.callback_query(BuyProductCallback.filter())
async def buy_product_handler(
    callback: CallbackQuery,
    callback_data: BuyProductCallback,
    user: UserModel,
    products_repo: FromDishka[ProductsRepo],
    products_service: FromDishka[ProductsService],
) -> None:
    product = await products_repo.get_one(callback_data.id)

    if product.stock > 0:
        if user.balance >= product.price:
            await products_service.buy_product(user.id, product.id, 1)
            text = "Товар оплачен и добавлен в корзину!"
        else:
            text = "Упс, у вас недостаточно <b>Иткоинов</b>!"
    else:
        text = "Упс, продукт уже раскупили"

    await callback.message.answer(text=text, reply_markup=view_shop_keyboard)

    await callback.message.delete()
