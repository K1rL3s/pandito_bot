from aiogram import F, Router
from aiogram.filters import MagicData

from .broadcast.dialogs import broadcast_dialog
from .broadcast.router import router as broadcast_router
from .logs.router import router as logs_router
from .money.router import router as money_router
from .panel.dialogs import admin_panel_dialog
from .panel.router import router as admin_panel_router
from .products.router import router as products_routes
from .qrcode.router import router as qrcodes_router
from .secret.router import router as secret_router
from .users.router import router as users_router


def include_admin_routers(root_router: Router) -> None:
    admin_router = Router(name=__file__)
    for observer in admin_router.observers.values():
        observer.filter(MagicData(F.user.role.is_not(None)))  # Фильтр на админку

    admin_router.include_routers(
        qrcodes_router,
        admin_panel_router,
        broadcast_router,
        logs_router,
        money_router,
        products_routes,
        users_router,
        secret_router,
    )
    _include_admin_dialogs(admin_router)

    root_router.include_router(admin_router)


def _include_admin_dialogs(router: Router) -> None:
    router.include_routers(
        admin_panel_dialog,
        broadcast_dialog,
    )
