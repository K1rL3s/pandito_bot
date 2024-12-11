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

from bot.keyboards.products import products_seller_keyboard
from bot.states import SalesmanCart, SalesmanShop
from core.services.products import ProductsService
from database.repos.products import ProductsRepo
from database.repos.purchases import PurchasesRepo
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.callback_query(F.data == "view_products_salesman")
async def view_products_salesman_handler(
    callback: CallbackQuery,
    products_repo: FromDishka[ProductsRepo],
) -> None:
    products = await products_repo.get_available()
    if products:
        text = "Выберите товар для продажи:"
        keyboard = products_seller_keyboard(products)
    else:
        text = "В магазине нет товаров в наличии."
        keyboard = None

    await callback.message.answer(text=text, reply_markup=keyboard)
    await callback.message.delete()


@router.callback_query(F.data.startswith("salesman_select_product_"))
async def salesman_select_product_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    text = "Введите id покупателя, которому нужно продать товар."
    await callback.message.answer(text=text)

    product_id = int(callback.data.split("_")[-1])
    await state.update_data(product_id=product_id)
    await state.set_state(SalesmanShop.buyer_id)


@router.message(SalesmanShop.buyer_id)
async def salesman_buyer_id_handler(
    message: Message,
    state: FSMContext,
    users_repo: FromDishka[UsersRepo],
    products_repo: FromDishka[ProductsRepo],
    products_service: FromDishka[ProductsService],
) -> None:
    buyer_id = message.text.strip()
    if not re.match(r"^\d+$", buyer_id):
        await message.answer("Неверный формат id! Попробуйте еще раз.")
        return

    buyer = await users_repo.get_by_id(int(buyer_id))
    if not buyer:
        await message.answer("Такого покупателя не существует.")
        return

    data = await state.get_data()
    product_id = int(data["product_id"])
    product = await products_repo.get_one(product_id)

    if buyer.balance < product.price:
        text = "У покупателя недостаточно средств"
    elif product.stock < 0:
        text = "Товара нет в наличии"
    else:
        await products_service.buy_product(buyer.id, product_id, 1)
        text = (
            f"Успех! {buyer.name} ({buyer.id}) купил {product.name} "
            f"за {product.price} Ит."
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад 🔙",
                    callback_data="view_products_salesman",
                ),
            ],
        ],
    )
    await message.answer(text=text, reply_markup=keyboard)

    await state.clear()


@router.callback_query(F.data == "members_purchases")
async def view_members_purchases_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.answer(
        "Введите id участника, чью корзину хотите просмотреть.",
    )
    await callback.message.delete()
    await state.set_state(SalesmanCart.buyer_id)


@router.message(SalesmanCart.buyer_id)
async def show_cart_handler(
    message: Message,
    state: FSMContext,
    users_repo: FromDishka[UsersRepo],
    purchases_repo: FromDishka[PurchasesRepo],
) -> None:
    buyer_id = message.text.strip()
    if not re.match(r"^\d+$", buyer_id):
        await message.answer("Неверный формат id! Попробуйте еще раз.")
        return

    slave = await users_repo.get_by_id(int(buyer_id))
    if not slave:
        await message.answer("Такого участника не существует.")
        return

    purchases = await purchases_repo.get_user_purchases(slave.id)

    if purchases:
        cart_text = "\n".join(
            [f"{product.name} x{purchase.quantity}" for product, purchase in purchases],
        )
        text = f"Корзина участника {slave.name}:\n\n{cart_text}"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Подтвердить",
                        callback_data=f"confirm_clear_cart_{buyer_id}",
                    ),
                ],
            ],
        )
    else:
        text = "Корзина пуста"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
            ],
        )

    await message.answer(text=text, reply_markup=keyboard)

    await state.clear()


@router.callback_query(F.data.startswith("confirm_clear_cart_"))
async def confirm_clear_cart_handler(
    callback: CallbackQuery,
    purchases_repo: FromDishka[PurchasesRepo],
) -> None:
    buyer_id = int(callback.data.split("_")[-1])

    await purchases_repo.clear_purchases(buyer_id)

    text = f"Корзина участника с id {buyer_id} успешно очищена!"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")],
        ],
    )

    await callback.message.answer(text=text, reply_markup=keyboard)
    await callback.message.delete()
