from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.products import BuyProductCallback, ViewProductCallback
from database.models import ProductModel

view_shop_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Магазин", callback_data="view_products")],
    ],
)


def products_keyboard(products: list[ProductModel]) -> InlineKeyboardMarkup:
    product_kb = [
        [
            InlineKeyboardButton(
                text=f"{product.name} — {product.price} Ит.",
                callback_data=ViewProductCallback(id=int(product.id)).pack(),
            ),
        ]
        for product in products
    ]
    product_kb.append(
        [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
    )
    return InlineKeyboardMarkup(inline_keyboard=product_kb)


def products_seller_keyboard(products: list[ProductModel]) -> InlineKeyboardMarkup:
    product_kb = [
        [
            InlineKeyboardButton(
                text=f"{product.name} - {product.price} Ит.",
                callback_data=f"salesman_select_product_{product.id}",
            ),
        ]
        for product in products
    ]
    product_kb.append(
        [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
    )
    return InlineKeyboardMarkup(inline_keyboard=product_kb)


def buy_product_keyboard(product: ProductModel) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Купить - {product.price} Ит.",
                    callback_data=BuyProductCallback(id=int(product.id)).pack(),
                ),
                InlineKeyboardButton(
                    text="🔙 Назад 🔙",
                    callback_data="view_products",
                ),
            ],
        ],
    )
