from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.users.view.states import ViewUserStates
from core.ids import UserId
from core.services.users import UsersService
from database.repos.users import UsersRepo


@inject
async def student_id_input_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    student_id = message.text.strip()
    view_user_id = dialog_manager.dialog_data["view_user_id"]
    user = await users_repo.get_by_student_id(student_id)
    if user and user.id != view_user_id:
        text = f"Такой номер студенческого уже занят: {user.id} {user.name}"
        await message.answer(text=text)
    else:
        dialog_manager.dialog_data["student_id"] = student_id
        await dialog_manager.next()


@inject
async def group_input_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    users_service: FromDishka[UsersService],
) -> None:
    group = message.text.strip()
    student_id: str = dialog_manager.dialog_data["student_id"]
    view_user_id: UserId = dialog_manager.dialog_data["view_user_id"]

    await users_service.set_lottery_info(
        view_user_id,
        student_id,
        group,
        message.from_user.id,
    )

    await dialog_manager.start(ViewUserStates.one, data={"view_user_id": view_user_id})
