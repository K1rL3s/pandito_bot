from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY
from aiogram.types import TelegramObject, User
from dishka import AsyncContainer

from database.repos.users import UsersRepo


class UserDbContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        from_user: User | None = data.get(EVENT_FROM_USER_KEY)
        if from_user is not None:
            container: AsyncContainer = data["dishka_container"]
            users_repo = await container.get(UsersRepo)
            db_user = await users_repo.get_one(from_user.id)
            if db_user is None:
                db_user = await users_repo.create(
                    tg_id=from_user.id,
                    name="",
                    balance=0,
                    is_admin=False,
                )
            data["user"] = db_user

        return await handler(event, data)
