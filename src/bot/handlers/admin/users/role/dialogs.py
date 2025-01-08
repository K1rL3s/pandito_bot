from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Group, Row
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data
from core.enums import RightsRole

from ..getters import user_short_link
from ..utils import _UserIdNameText, on_go_view_user
from .states import RoleUserStates

user_role_window = Window(
    _UserIdNameText,
    Group(
        *[Button(Const(role), id=f"role_{role}") for role in RightsRole.values()],
        width=2,
    ),
    Button(Const("⏪ Юзер"), id="back", on_click=on_go_view_user),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=user_short_link,
    state=RoleUserStates.select,
)

set_role_window = Window(
    Format(
        "Уверены, что хотите установить роль {dialog_manager[dialog_data][new_role]} "
        "пользователю {view_user.id} - {view_user.name}?",
    ),
    Row(
        Back(Const("⏪ Роли")),
        Button(Const("✅ Подтверждаю"), id="confirm", on_click=None),
    ),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=user_short_link,
    state=RoleUserStates.role,
)

set_role_confirm = Window(
    Const("Ок!"),
    state=RoleUserStates.confirm,
)

user_role_dialog = Dialog(
    user_role_window,
    set_role_window,
    set_role_confirm,
    on_start=on_start_update_dialog_data,
)
