from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton
from bot.enums import BotWindow
from bot.filters.roles import IsWithRole

from .getters import get_user_info
from .on_actions import on_cart, on_help, on_shop, on_transfer_funds
from .states import MenuStates

menu_dialog = Dialog(
    Window(
        Const("<b>Главное меню</b>\n"),
        Format("Ваш ID: <code>{user_id}</code> (/id)"),
        Format("Баланс: {balance} <b>Пятаков</b>\n"),
        Format("Вы - <u>{role}</u>", when=IsWithRole()),
        Group(
            Button(Const("🛍️ Магазин"), id=BotWindow.SHOP, on_click=on_shop),
            Button(Const("🧺 Корзина"), id=BotWindow.CART, on_click=on_cart),
            Button(
                Const("💸 Перевод"),
                id=BotWindow.TRANSFER,
                on_click=on_transfer_funds,
            ),
            Button(Const("🆘 Помощь"), id=BotWindow.HELP, on_click=on_help),
            width=2,
        ),
        GoToAdminPanelButton(when=IsWithRole()),
        getter=get_user_info,
        state=MenuStates.menu,
    ),
)
