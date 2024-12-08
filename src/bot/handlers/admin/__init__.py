from aiogram import Dispatcher, F, Router
from aiogram.filters import MagicData

from .broadcast import router as broadcast_router
from .logs import router as logs_router
from .money import router as money_router
from .products import router as products_routes
from .users import router as users_router


def include_admin_routers(dp: Dispatcher) -> None:
    admin_router = Router(name=__file__)

    for observer in admin_router.observers.values():
        observer.filter(MagicData(F.user.is_admin))  # Фильтр на админку

    admin_router.include_routers(
        broadcast_router,
        logs_router,
        money_router,
        products_routes,
        users_router,
    )

    dp.include_router(admin_router)
