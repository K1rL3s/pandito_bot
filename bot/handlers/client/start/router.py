from aiogram import Router

from .register import router as register_router
from .start import router as start_router

router = Router(name=__file__)


router.include_routers(
    start_router,
    register_router,
)
