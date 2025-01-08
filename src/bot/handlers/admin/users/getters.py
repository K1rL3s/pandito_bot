from typing import Any

from aiogram_dialog import DialogManager

from database.models import UserModel


async def user_short_link(
    dialog_manager: DialogManager,
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.dialog_data["view_user"]
    role = user.role or "user"
    return {"view_user": user, "role": role}
