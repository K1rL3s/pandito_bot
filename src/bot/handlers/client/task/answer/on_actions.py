from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.exceptions import WrongTaskAnswer
from core.services.tasks import TasksService
from database.models import UserModel

from ..answer.states import AnswerTaskStates


@inject
async def on_answer_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    tasks_service: FromDishka[TasksService],
) -> None:
    user: UserModel = dialog_manager.middleware_data["user"]
    try:
        title, reward = await tasks_service.reward_for_task_by_pharse(
            user.id,
            message.text,
        )
    except WrongTaskAnswer:
        return await dialog_manager.start(AnswerTaskStates.fail)

    return await dialog_manager.start(
        AnswerTaskStates.ok,
        data={"reward": reward, "title": title},
    )
