from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.client.menu.states import MenuStates
from core.services.tasks import TasksService

from ..answer.states import AnswerTaskStates


@inject
async def on_cancel_task(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    tasks_service: FromDishka[TasksService],
) -> None:
    await tasks_service.cancel_active_task(callback.from_user.id)
    await dialog_manager.start(MenuStates.menu)


async def on_answer(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(AnswerTaskStates.wait)
