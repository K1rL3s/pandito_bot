from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .on_actions import on_go_view_user

GoToUserButton = Button(Const("⏪ Юзер"), id="back", on_click=on_go_view_user)
