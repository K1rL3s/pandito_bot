from aiogram import Dispatcher, F, Router
from aiogram.filters import MagicData

from .broadcast.router import router as broadcast_router
from .logs.router import router as logs_router
from .money.router import router as money_router
from .products.router import router as products_routes
from .qrcode.router import router as qrcodes_router
from .secret.router import router as secret_router
from .users.router import router as users_router


def include_admin_routers(dp: Dispatcher) -> None:
    admin_router = Router(name=__file__)

    for observer in admin_router.observers.values():
        observer.filter(MagicData(F.user.is_admin))  # Фильтр на админку

    admin_router.include_routers(
        qrcodes_router,
        broadcast_router,
        logs_router,
        money_router,
        products_routes,
        users_router,
        secret_router,
    )

    dp.include_router(admin_router)
