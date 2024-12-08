from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.products import BuyProductCallback, ViewProductCallback
from database.repos.database import Database

router = Router(name=__file__)


@router.callback_query(F.data == "view_products")
async def view_products_handler(callback: CallbackQuery, db: Database):
    await callback.answer()
    products = await db.get_available()
    user = await db.get_user(callback.from_user.id)
    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        ],
    )
    if products:
        product_kb = [
            [
                InlineKeyboardButton(
                    text=f"{product['name']} — {product['price']} Ит.",
                    callback_data=ViewProductCallback(id=int(product["id"])).pack(),
                ),
            ]
            for product in products
        ]
        product_kb.append(
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        )
        p_kb = InlineKeyboardMarkup(inline_keyboard=product_kb)

        await callback.message.answer(
            f"Список товаров 🛍️\n\nБаланс: {user['balance']} Ит.",
            reply_markup=p_kb,
        )
    else:
        await callback.message.answer(
            "Упс, сейчас ничего в наличии нет",
            reply_markup=c_bk,
        )
    await callback.message.delete()


@router.callback_query(ViewProductCallback.filter())
async def view_one_product_handler(
    callback: CallbackQuery,
    callback_data: ViewProductCallback,
    db: Database,
) -> None:
    await callback.answer()
    await callback.message.delete()
    product = await db.get_one(callback_data.id)
    if int(product["stock"]) > 0:
        b_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Купить - {product['price']} Ит.",
                        callback_data=BuyProductCallback(id=int(product["id"])).pack(),
                    ),
                    InlineKeyboardButton(
                        text="🔙 Назад 🔙",
                        callback_data="view_products",
                    ),
                ],
            ],
        )
        await callback.message.answer(
            f"{product['id']}. <b>{product['name']}</b>\n\n{product['description']}",
            reply_markup=b_kb,
            parse_mode="HTML",
        )
    else:
        c_bk = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔙 Назад 🔙",
                        callback_data="view_products",
                    ),
                ],
            ],
        )
        await callback.message.answer("Упс, уже раскупили", reply_markup=c_bk)


@router.callback_query(BuyProductCallback.filter())
async def buy_product_handler(
    callback: CallbackQuery,
    callback_data: BuyProductCallback,
    db: Database,
):
    await callback.answer()
    product = await db.get_one(callback_data.id)
    user = await db.get_user(callback.from_user.id)
    shop_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Магазин", callback_data="view_products")],
        ],
    )
    if int(product["stock"]) > 0:
        if user["balance"] >= product["price"]:
            await db.buy_product(int(user["id"]), int(product["id"]), 1)
            await callback.message.answer(
                "Товар оплачен и добавлен в корзину!",
                reply_markup=shop_bk,
            )
        else:
            await callback.message.answer(
                "Упс, у вас недостаточно <b>Иткоинов</b>!",
                reply_markup=shop_bk,
                parse_mode="HTML",
            )
    else:
        await callback.message.answer(
            "Упс, продукт уже раскупили",
            reply_markup=shop_bk,
        )
    await callback.message.delete()
