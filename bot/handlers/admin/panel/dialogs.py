from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton

from .on_actions import on_go_to_broadcast
from .states import AdminPanelStates

admin_panel_window = Window(
    Format("❗Админ-панель, вы - <u>{middleware_data[user].role}</u>"),
    Group(
        Button(Const("📢 Рассылка"), id="broadcast", on_click=on_go_to_broadcast),
        Button(Const("👥 Пользователи"), id="users"),
        Button(Const("🛍️ Товары"), id="products"),
        Button(Const("🤫 Секреты"), id="secrets"),
        Button(Const("🧠 Задания"), id="tasks"),
        width=2,
    ),
    GoToMenuButton(),
    state=AdminPanelStates.panel,
)

admin_panel_dialog = Dialog(admin_panel_window)
