from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.enums import SlashCommand
from bot.handlers.client.menu.states import MenuStates
from bot.utils.qrcode import send_and_save_user_qrcode
from core.services.qrcodes import QRCodeService
from database.models import UserModel
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.message(Command(SlashCommand.ID))
async def show_my_id_as_qrcode(
    message: Message,
    bot: Bot,
    dialog_manager: DialogManager,
    user: UserModel,
    qrcode_service: FromDishka[QRCodeService],
    users_repo: FromDishka[UsersRepo],
) -> None:
    text = (
        "Покажи это организатору =)\n\n"
        f"ID: <code>{message.from_user.id}</code> ({message.from_user.id:_})\n\n"
    )

    if user.qrcode_image_id:
        await message.answer_photo(photo=user.qrcode_image_id, caption=text)
        await dialog_manager.start(state=MenuStates.menu)
        return

    await send_and_save_user_qrcode(
        qrcode_service=qrcode_service,
        users_repo=users_repo,
        caption=text,
        bot=bot,
        save_to=user.id,
        send_to=user.id,
    )
    await dialog_manager.start(state=MenuStates.menu)
