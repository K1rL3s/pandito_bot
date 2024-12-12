from aiogram import Dispatcher

from .admin import include_admin_routers
from .client import include_client_routers
from .exceptions import router as exceptions_router
from .unknown_message import router as unknown_message_router


def include_routers(dp: Dispatcher) -> None:
    include_admin_routers(dp)
    include_client_routers(dp)
    dp.include_routers(
        unknown_message_router,
        exceptions_router,
    )
