from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import UserId
from database.repos.tasks import TasksRepo


@inject
async def get_active_task(
    dialog_manager: DialogManager,
    tasks_repo: FromDishka[TasksRepo],
    **__: Any,
) -> dict[str, Any]:
    view_user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    task = await tasks_repo.get_active_task(view_user_id)
    return {"task": task}
