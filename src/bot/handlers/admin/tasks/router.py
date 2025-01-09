from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.enums import SlashCommand
from bot.handlers.admin.tasks.view.states import ViewTasksStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.TASKS))
async def list_tasks_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=ViewTasksStates.list)
