import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bot.states import SalesmanCart, SalesmanShop
from database.repos.database import Database

router = Router(name=__file__)


@router.callback_query(F.data == "view_products_salesman")
async def view_products_salesman_handler(callback: CallbackQuery, db: Database):
    await callback.answer()
    await callback.message.delete()
    products = await db.get_available()  # Получаем список товаров из базы данных
    if products:
        product_kb = [
            [
                InlineKeyboardButton(
                    text=f"{product['name']} - {product['price']} Ит.",
                    callback_data=f"salesman_select_product_{product['id']}",
                ),
            ]
            for product in products
        ]
        product_kb.append(
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        )
        p_kb = InlineKeyboardMarkup(inline_keyboard=product_kb)

        await callback.message.answer("Выберите товар для продажи:", reply_markup=p_kb)
    else:
        await callback.message.answer("В магазине нет товаров в наличии.")


@router.callback_query(F.data.startswith("salesman_select_product_"))
async def salesman_select_product_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    product_id = int(callback.data.split("_")[-1])
    await state.update_data(product_id=product_id)
    await state.set_state(SalesmanShop.buyer_id)
    await callback.message.answer(
        "Введите id покупателя, которому нужно продать товар.",
    )


@router.message(SalesmanShop.buyer_id)
async def salesman_buyer_id_handler(message: Message, state: FSMContext, db: Database):
    buyer_id = message.text.strip()
    if not re.match(r"^\d+$", buyer_id):
        await message.answer("Неверный формат id! Попробуйте еще раз.")
        return

    user = await db.get_user_by_id(int(buyer_id))
    if not user:
        await message.answer("Такого покупателя не существует.")
        return

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад 🔙",
                    callback_data="view_products_salesman",
                ),
            ],
        ],
    )

    data = await state.get_data()
    product_id = data["product_id"]
    product = await db.get_product(product_id)

    if user["balance"] >= product["price"]:
        # Если средств хватает, списываем деньги и уменьшаем количество товара
        await db.buy_product(int(buyer_id), int(product_id), 1)

        await message.answer(
            f"Успех! {user['name']} купил {product['name']} за "
            f"{product['price']} Ит.",
            reply_markup=c_bk,
        )
    else:
        await message.answer("У покупателя недостаточно средств.", reply_markup=c_bk)

    await state.clear()


@router.callback_query(F.data == "members_purchases")
async def view_members_purchases_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.set_state(SalesmanCart.buyer_id)
    await callback.message.answer(
        "Введите id участника, чью корзину хотите просмотреть.",
    )


@router.message(SalesmanCart.buyer_id)
async def show_cart_handler(message: Message, state: FSMContext, db: Database):
    buyer_id = message.text.strip()
    if not re.match(r"^\d+$", buyer_id):
        await message.answer("Неверный формат id! Попробуйте еще раз.")
        return

    user = await db.get_user_by_id(int(buyer_id))
    if not user:
        await message.answer("Такого участника не существует.")
        return

    purchases = await db.get_user_purchases(int(buyer_id))

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        ],
    )

    if purchases:
        cart_text = "\n".join(
            [
                f"{purchase['product_name']} x{purchase['quantity_purchased']}"
                for purchase in purchases
            ],
        )
        confirm_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Подтвердить",
                        callback_data=f"confirm_clear_cart_{buyer_id}",
                    ),
                ],
            ],
        )
        await message.answer(
            f"Корзина участника {user['name']}:\n\n{cart_text}",
            reply_markup=confirm_kb,
        )
    else:
        await message.answer("Корзина пуста.", reply_markup=c_bk)

    await state.clear()


@router.callback_query(F.data.startswith("confirm_clear_cart_"))
async def confirm_clear_cart_handler(callback: CallbackQuery, db: Database):
    buyer_id = int(callback.data.split("_")[-1])

    # Очищаем корзину участника в базе данных
    await db.clear_purchases(buyer_id)

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        ],
    )

    await callback.message.answer(
        f"Корзина участника с id {buyer_id} успешно очищена!",
        reply_markup=c_bk,
    )
    await callback.message.delete()
