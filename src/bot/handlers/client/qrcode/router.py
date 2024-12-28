from aiogram import Bot, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import BufferedInputFile, Message
from dishka import FromDishka

from bot.enums import SlashCommand
from core.services.qrcodes import QRCodeService
from database.models import UserModel
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.message(Command(SlashCommand.ID), StateFilter(None))
async def show_my_id_as_qrcode(
    message: Message,
    bot: Bot,
    user: UserModel,
    qrcode_service: FromDishka[QRCodeService],
    users_repo: FromDishka[UsersRepo],
) -> None:
    text = (
        "Покажи это организатору =)\n\n"
        f"ID: <code>{message.from_user.id}</code> ({message.from_user.id:_})"
    )

    if user.qrcode_image_id:
        await message.answer_photo(photo=user.qrcode_image_id, caption=text)
        return

    bot_name = (await bot.me()).username
    qrcode = qrcode_service.generate_qrcode(user.id, bot_name)
    photo = BufferedInputFile(qrcode.getvalue(), f"qrcode_{user.id}.png")
    bot_message = await message.answer_photo(photo=photo, caption=text)
    qrcode_image_id = bot_message.photo[-1].file_id
    await users_repo.set_qrcode_image_id(user.id, qrcode_image_id)
