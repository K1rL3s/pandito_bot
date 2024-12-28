from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.dialogs.flags import FORCE_GET_USER_KEY
from database.models import UserModel
from database.repos.users import UsersRepo


@inject
async def get_user_info(
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["user"]
    if dialog_manager.start_data and dialog_manager.start_data.get(FORCE_GET_USER_KEY):
        user = await users_repo.get_by_id(user.id)
    return {"user_id": user.id, "balance": user.balance, "role": user.role}
