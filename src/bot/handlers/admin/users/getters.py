from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import UserId
from database.repos.users import UsersRepo


@inject
async def user_short_link(
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
    **__: Any,
) -> dict[str, Any]:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    user = await users_repo.get_by_id(user_id)
    role = user.role or "user"
    return {"view_user": user, "role": role}
