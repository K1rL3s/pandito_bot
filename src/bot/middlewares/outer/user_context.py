from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY
from aiogram.types import TelegramObject, User

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
            user_repo: UsersRepo = data["user_repo"]
            db_user = await user_repo.get_user(from_user.id)
            if db_user is None:
                db_user = await user_repo.create_user(
                    from_user.id,
                    from_user.username or from_user.full_name,
                )
            data["user"] = db_user

        return await handler(event, data)
