from aiogram import F, Router
from aiogram.filters import Command, CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.enums import SlashCommand
from bot.handlers.client.task.start.states import StartTaskStates
from bot.handlers.client.task.view.states import ViewTaskStates
from core.services.qrcodes import TaskIdPrefix
from database.repos.tasks import TasksRepo

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith(TaskIdPrefix)),
    MagicData(F.command.args.as_("task_deeplink")),
)
async def start_task_by_deeplink(
    message: Message,
    task_deeplink: str,
    dialog_manager: DialogManager,
    task_repo: FromDishka[TasksRepo],
) -> None:
    task_id = task_deeplink.lstrip(TaskIdPrefix)

    if await task_repo.get_by_id(task_id):
        if not await task_repo.is_task_claimed(message.from_user.id, task_id):
            await dialog_manager.start(StartTaskStates.wait, data={"task_id": task_id})

    await message.delete()


@router.message(Command(SlashCommand.TASK))
async def view_active_task(
    message: Message,
    dialog_manager: DialogManager,
    task_repo: FromDishka[TasksRepo],
) -> None:
    if await task_repo.get_active_task(message.from_user.id):
        await dialog_manager.start(ViewTaskStates.task)
    else:
        await message.delete()
