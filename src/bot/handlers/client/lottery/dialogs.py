from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton

from .getters import get_lottery_info
from .states import ViewLotteryStates

lottery_info_window = Window(
    Format("🎟️ В лотерее сейчас участвует {total_students} студентов\n"),
    Const("Чтобы принять участие, подойте на стойку около ..."),
    GoToMenuButton(),
    getter=get_lottery_info,
    state=ViewLotteryStates.view,
)

lottery_dialog = Dialog(lottery_info_window)
