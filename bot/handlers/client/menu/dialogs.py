from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format

from bot.enums import BotWindow

from .getters import get_user_info
from .states import MenuState

menu_dialog = Dialog(
    Window(
        Const("<b>Главное меню</b>\n"),
        Format("Ваш ID: <code>{user_id}</code> (/id)"),
        Format("Баланс: {balance} <b>Ит.</b>\n"),
        Format("<u>Вы - {role}</u>", when=F["start_data"]["role"]),
        Group(
            Button(Const("Магазин 🛍️"), id=BotWindow.SHOP),
            Button(Const("Корзина 🧺"), id=BotWindow.CART),
            Button(Const("Перевод 💸"), id=BotWindow.TRANSFER_FUNDS),
            Button(Const("Помощь 🆘"), id=BotWindow.HELP),
            Button(
                Const("Админ панель ❗"),
                id=BotWindow.ADMIN_PANEL,
                when=F["start_data"]["role"],
            ),
            width=2,
        ),
        getter=get_user_info,
        state=MenuState.menu,
    ),
)
