from aiogram import Dispatcher

from .cancel import router as cancel_router
from .menu import router as menu_router
from .products import router as product_router
from .purchases import router as purchases_router
from .register import router as register_router
from .secret import router as secret_router
from .seller import router as seller_router
from .stages import router as stages_router
from .start import router as start_router
from .transfer_funds import router as transfer_funds_router


def include_client_routers(dp: Dispatcher) -> None:
    dp.include_routers(  # TODO: проверить порядок роутеров
        cancel_router,
        menu_router,
        product_router,
        purchases_router,
        register_router,
        secret_router,
        seller_router,
        stages_router,
        start_router,
        transfer_funds_router,
    )
