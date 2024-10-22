import asyncio
from datetime import timedelta
from typing import Any, Callable

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis


def fn(*_):
    pass


def create_storage(
    redis: Redis | None = None,
    state_ttl: int | timedelta | None = None,
    data_ttl: int | timedelta | None = None,
) -> BaseStorage:
    if redis:
        return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl)
    return MemoryStorage()


def create_dispatcher(
    debug_name: str,
    storage: BaseStorage,
    include_routers: Callable[[Dispatcher], None] = fn,
    include_middlewares: Callable[[Dispatcher], None] = fn,
    on_startup: Callable[..., Any] = fn,
    on_shutdown: Callable[..., Any] = fn,
) -> Dispatcher:
    """Создаёт диспетчер и регистрирует все роуты."""
    dp = Dispatcher(
        name=debug_name,
        storage=storage,
    )

    include_routers(dp)
    include_middlewares(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return dp
