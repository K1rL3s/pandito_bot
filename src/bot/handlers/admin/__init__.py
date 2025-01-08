from aiogram import F, Router
from aiogram.filters import MagicData

from .broadcast.dialogs import broadcast_dialog
from .broadcast.router import router as broadcast_router
from .logs.router import router as logs_router
from .money.router import router as money_router
from .panel.dialogs import admin_panel_dialog
from .panel.router import router as admin_panel_router
from .products.router import router as products_routes
from .secret.dialogs import create_secret_dialog, view_secrets_dialog
from .secret.router import router as secret_router
from .users.cart.dialogs import user_cart_dialog
from .users.role.dialogs import user_role_dialog
from .users.router import router as users_router
from .users.view.dialogs import view_user_dialog


def include_admin_routers(root_router: Router) -> None:
    admin_router = Router(name=__file__)
    for observer in admin_router.observers.values():
        observer.filter(MagicData(F.user.role.is_not(None)))  # Фильтр на админку

    admin_router.include_routers(
        users_router,
        admin_panel_router,
        broadcast_router,
        logs_router,
        money_router,
        products_routes,
        secret_router,
    )

    root_router.include_router(admin_router)


def include_admin_dialogs(root_router: Router) -> None:
    admin_router = Router(name=__file__)
    for observer in admin_router.observers.values():
        observer.filter(MagicData(F.user.role.is_not(None)))  # Фильтр на админку

    admin_router.include_routers(
        admin_panel_dialog,
        broadcast_dialog,
        view_secrets_dialog,
        create_secret_dialog,
        view_user_dialog,
        user_cart_dialog,
        user_role_dialog,
    )

    root_router.include_router(admin_router)
