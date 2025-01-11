from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.users.view.states import ViewUserStates
from core.ids import UserId
from core.services.broadcast import Broadcaster
from core.services.tasks import TasksService


@inject
async def on_confirm_task(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    tasks_service: FromDishka[TasksService],
    broadcaster: FromDishka[Broadcaster],
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    master_id: UserId = callback.from_user.id

    title, reward = await tasks_service.reward_for_task_by_stager(user_id, master_id)

    text = f"💵 Задание «{title}» завершено! Начислено {reward} Пятаков"
    await broadcaster.one_notify(text, user_id)

    await dialog_manager.start(ViewUserStates.one, data={"view_user_id": user_id})
