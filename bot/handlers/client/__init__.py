from aiogram import Dispatcher

from .cancel import router as cancel_router
from .help.router import router as help_router
from .menu.router import router as menu_router
from .products.router import router as product_router
from .purchases.router import router as purchases_router
from .qrcodes.router import router as qrcodes_router
from .secret.router import router as secret_router
from .seller.router import router as seller_router
from .stages.router import router as stages_router
from .start.router import router as start_router
from .transfer_funds.router import router as transfer_funds_router


def include_client_routers(dp: Dispatcher) -> None:
    dp.include_routers(  # TODO: проверить порядок роутеров
        cancel_router,
        menu_router,
        product_router,
        purchases_router,
        qrcodes_router,
        secret_router,
        seller_router,
        stages_router,
        start_router,
        transfer_funds_router,
        help_router,
    )
