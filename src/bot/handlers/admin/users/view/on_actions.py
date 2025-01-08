from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from database.models import UserModel
from database.repos.users import UsersRepo

from ..cart.states import CartUserStates
from ..role.states import RoleUserStates


@inject
async def id_input_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    user_id = int(message.text)

    user = await users_repo.get_by_id(user_id)
    if user is None:
        text = f"Пользователя с ID {user_id} не существует :("
        await message.reply(text=text)
        return

    dialog_manager.dialog_data["view_user"] = user
    await dialog_manager.next()


async def on_check_cart(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserModel = dialog_manager.dialog_data["view_user"]
    await dialog_manager.start(state=CartUserStates.cart, data={"view_user": user})


async def on_set_role(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserModel = dialog_manager.dialog_data["view_user"]
    await dialog_manager.start(state=RoleUserStates.select, data={"view_user": user})


async def on_check_role(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserModel = dialog_manager.dialog_data["view_user"]
    await dialog_manager.start(state=RoleUserStates.role, data={"view_user": user})
