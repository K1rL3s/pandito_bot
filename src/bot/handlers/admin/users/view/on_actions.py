from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.utils.qrcode import send_and_save_user_qrcode
from core.services.qrcodes import QRCodeService
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


@inject
async def on_view_qrcode(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    qrcode_service: FromDishka[QRCodeService],
    users_repo: FromDishka[UsersRepo],
) -> None:
    user: UserModel = dialog_manager.dialog_data["view_user"]
    text = f"ID: <code>{user.id}</code> ({user.id:_})\n\n"
    if user.qrcode_image_id:
        await callback.message.answer_photo(
            photo=user.qrcode_image_id,
            caption=text,
        )
    else:
        await send_and_save_user_qrcode(
            qrcode_service=qrcode_service,
            users_repo=users_repo,
            caption=text,
            bot=callback.bot,
            save_to=user.id,
            send_to=callback.from_user.id,
        )

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND


async def on_check_role(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserModel = dialog_manager.dialog_data["view_user"]
    await dialog_manager.start(state=RoleUserStates.role, data={"view_user": user})
