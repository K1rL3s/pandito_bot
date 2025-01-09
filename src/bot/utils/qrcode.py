from aiogram import Bot
from aiogram.types import BufferedInputFile

from core.ids import TaskId, UserId
from core.services.qrcodes import QRCodeService
from database.repos.tasks import TasksRepo
from database.repos.users import UsersRepo


async def send_and_save_user_qrcode(
    qrcode_service: QRCodeService,
    users_repo: UsersRepo,
    caption: str,
    bot: Bot,
    save_to: UserId,
    send_to: UserId,
) -> None:
    qrcode = qrcode_service.user_id_qrcode(save_to)
    photo = BufferedInputFile(qrcode.getvalue(), f"qrcode_user{save_to}.png")
    bot_message = await bot.send_photo(chat_id=send_to, photo=photo, caption=caption)
    qrcode_image_id = bot_message.photo[-1].file_id
    await users_repo.set_qrcode_image_id(save_to, qrcode_image_id)


async def send_and_save_task_qrcode(
    qrcode_service: QRCodeService,
    tasks_repo: TasksRepo,
    caption: str,
    bot: Bot,
    task_id: TaskId,
    send_to: UserId,
) -> None:
    qrcode = qrcode_service.task_id_qrcode(task_id)
    photo = BufferedInputFile(qrcode.getvalue(), f"qrcode_task{task_id}.png")
    bot_message = await bot.send_photo(chat_id=send_to, photo=photo, caption=caption)
    qrcode_image_id = bot_message.photo[-1].file_id
    await tasks_repo.set_qrcode_image_id(task_id, qrcode_image_id)
