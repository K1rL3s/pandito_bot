from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton
from bot.filters.roles import IsAdmin, IsSeller, IsStager, IsWithRole

from .on_actions import (
    on_go_to_broadcast,
    on_go_to_secrets,
    on_go_to_shop,
    on_go_to_tasks,
    on_go_to_view_users,
)
from .states import AdminPanelStates

admin_panel_window = Window(
    Format("❗Админ-панель, вы - <u>{middleware_data[user].role}</u>"),
    Group(
        Button(
            Const("📢 Рассылка"),
            id="broadcast",
            on_click=on_go_to_broadcast,
            when=IsAdmin(),
        ),
        Button(
            Const("👥 Пользователи"),
            id="users",
            on_click=on_go_to_view_users,
            when=IsWithRole(),
        ),
        Button(
            Const("🛍️ Товары"),
            id="products",
            on_click=on_go_to_shop,
            when=IsSeller(),
        ),
        Button(
            Const("🤫 Секреты"),
            id="secrets",
            on_click=on_go_to_secrets,
            when=IsAdmin(),
        ),
        Button(
            Const("🧠 Задания"),
            id="tasks",
            on_click=on_go_to_tasks,
            when=IsStager(),
        ),
        width=2,
    ),
    GoToMenuButton(),
    state=AdminPanelStates.panel,
)

admin_panel_dialog = Dialog(admin_panel_window)
