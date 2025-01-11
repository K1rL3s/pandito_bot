from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton

from .getters import get_lottery_info
from .states import ViewLotteryStates

lottery_info_window = Window(
    Format("🎟️ В лотереи сейчас участвует {total_students} студентов"),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_lottery_info,
    state=ViewLotteryStates.view,
)

lottery_info_dialog = Dialog(lottery_info_window)
