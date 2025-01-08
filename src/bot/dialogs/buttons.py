from typing import Any

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.dialogs.on_actions import on_empty_button, on_go_to_admin_panel, on_go_to_menu


class GoToMenuButton(Button):
    def __init__(self, text: str = "🏠 В меню", **kwargs: Any) -> None:
        super().__init__(
            text=Const(text),
            id="to_menu",
            on_click=on_go_to_menu,
            **kwargs,
        )


class GoToAdminPanelButton(Button):
    def __init__(self, text: str = "❗ Админ панель", **kwargs: Any) -> None:
        super().__init__(
            text=Const(text),
            id="to_admin_panel",
            on_click=on_go_to_admin_panel,
            **kwargs,
        )


class EmptyButton(Button):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            text=Const(" "),
            id="empty",
            on_click=on_empty_button,
            **kwargs,
        )