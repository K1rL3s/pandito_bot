from aiogram import F, Router
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.filters import CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.handlers.admin.users.view.states import ViewUserStates
from core.services.qrcodes import UserIdPrefix
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith(UserIdPrefix)),
    MagicData(F.command.args.as_("user_deeplink")),
)
async def open_user_by_deeplink(
    message: Message,
    user_deeplink: str,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    user_id = user_deeplink.lstrip(UserIdPrefix)
    if not user_id.isdigit():
        raise CancelHandler

    user = await users_repo.get_by_id(int(user_id))
    if user is None:
        await message.answer(f"Юзер c ID {user_id} не найден")

    await dialog_manager.start(state=ViewUserStates.one, data={"view_user_id": user.id})
