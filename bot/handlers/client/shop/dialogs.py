import operator

from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import EmptyButton, GoToMenuButton
from bot.dialogs.on_actions import on_go_to_products

from .getters import get_available_products, get_one_product
from .on_actions import on_buy_product, on_view_product_selected
from .states import ShopStates

view_available_products_window = Window(
    Format(
        "Список товаров 🛍️\n\n"
        "В наличии <b>{products_len}</b> наименований "
        "в количестве <b>{total_stock}</b> штук\n"
        "Баланс: {middleware_data[user].balance} Ит.",
    ),
    Column(
        Select(
            Format("{item.name} — {item.price} Ит."),
            id="available_products",
            item_id_getter=operator.attrgetter("id"),
            items="products",
            type_factory=int,
            on_click=on_view_product_selected,
        ),
        when=F["products"].is_not(None),
    ),
    EmptyButton(when=F["products"].is_not(None)),
    GoToMenuButton(),
    state=ShopStates.list,
    getter=get_available_products,
)

view_one_product_window = Window(
    Format(
        "<b>{product.id}) {product.name}</b>\n"
        "<i>В наличии {product.stock} шт.</i>\n\n"
        "{product.description}",
    ),
    Button(Const("💵 Купить"), id="buy", on_click=on_buy_product),
    Back(Const("🔙 Все товары")),
    getter=get_one_product,
    state=ShopStates.one,
)

final_window = Window(
    Format("{dialog_data[final_message]}"),
    Button(Const("🛍️ Все товары"), id="to_products", on_click=on_go_to_products),
    GoToMenuButton(),
    state=ShopStates.final,
)


shop_dialog = Dialog(
    view_available_products_window,
    view_one_product_window,
    final_window,
)
