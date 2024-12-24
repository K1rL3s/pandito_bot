import logging
from dataclasses import dataclass

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramNotFound

from database.repos.users import UsersRepo


@dataclass
class BroadcastResult:
    ok: int
    fail: int

    @property
    def total(self) -> int:
        return self.ok + self.fail


class Broadcaster:  # TODO ускорить (очередь?)
    def __init__(self, users_repo: UsersRepo) -> None:
        self.users_repo = users_repo

    async def broadcast(self, bot: Bot, message: str) -> BroadcastResult:
        ok = fail = 0

        users = await self.users_repo.get_active()
        for user in users:
            try:
                await bot.send_message(chat_id=user.id, text=message)
                ok += 1
            except (TelegramNotFound, TelegramForbiddenError):
                await self.users_repo.change_active(user.id, False)
                fail += 1
            except Exception as e:  # noqa: BLE001
                logging.error(f"Ошибка во время рассылки: {type(e).__name__}('{e}')")
                fail += 1

        return BroadcastResult(ok, fail)
