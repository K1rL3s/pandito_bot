from aiogram import Dispatcher

from .admin import include_admin_routers
from .client import include_client_routers
from .unknown_message import router as unknown_message_router


def include_routers(dp: Dispatcher) -> None:
    include_client_routers(dp)
    include_admin_routers(dp)
    dp.include_router(unknown_message_router)
