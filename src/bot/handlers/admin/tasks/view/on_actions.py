from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.tasks.create.states import CreateTaskStates
from bot.handlers.admin.tasks.view.states import ViewTasksStates
from bot.utils.qrcode import send_and_save_task_qrcode
from core.ids import TaskId
from core.services.qrcodes import QRCodeService
from core.services.tasks import TasksService
from database.models import UserModel
from database.repos.tasks import TasksRepo


async def on_task_selected(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    dialog_manager.dialog_data["task_id"] = item_id
    await dialog_manager.next()


async def on_create_task(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=CreateTaskStates.title)


@inject
async def on_view_qrcode(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    qrcode_service: FromDishka[QRCodeService],
    tasks_repo: FromDishka[TasksRepo],
) -> None:
    task_id: TaskId = dialog_manager.dialog_data["task_id"]
    text = f"ID: <code>{task_id}</code>"
    task = await tasks_repo.get_by_id(task_id)

    if task.qrcode_image_id:
        await callback.message.answer_photo(
            photo=task.qrcode_image_id,
            caption=text,
        )
    else:
        await send_and_save_task_qrcode(
            qrcode_service=qrcode_service,
            tasks_repo=tasks_repo,
            caption=text,
            bot=callback.bot,
            task_id=task.id,
            send_to=callback.from_user.id,
        )

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND


@inject
async def on_confirm_delete_task(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    tasks_service: FromDishka[TasksService],
) -> None:
    task_id: TaskId = dialog_manager.dialog_data["task_id"]
    master: UserModel = dialog_manager.middleware_data["user"]
    await tasks_service.delete(task_id, master.id)
    await dialog_manager.start(state=ViewTasksStates.list)
