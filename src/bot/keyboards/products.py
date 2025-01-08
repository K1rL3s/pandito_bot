from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import ProductModel


def products_seller_keyboard(products: list[ProductModel]) -> InlineKeyboardMarkup:
    product_kb = [
        [
            InlineKeyboardButton(
                text=f"{product.name} - {product.price} Пятаков",
                callback_data=f"salesman_select_product_{product.id}",
            ),
        ]
        for product in products
    ]
    product_kb.append(
        [InlineKeyboardButton(text="⏪ Назад ⏪", callback_data="cancel")],
    )
    return InlineKeyboardMarkup(inline_keyboard=product_kb)
