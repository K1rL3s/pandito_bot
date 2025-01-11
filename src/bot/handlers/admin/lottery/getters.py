from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from database.repos.users import UsersRepo


@inject
async def get_lottery_info(
    users_repo: FromDishka[UsersRepo],
    **__: Any,
) -> dict[str, Any]:
    lottery = await users_repo.get_lottery()
    return {"total_students": len(lottery)}
