from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from database.repos.purchases import PurchasesRepo


async def on_clear_cart(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    pass


@inject
async def on_clear_cart_confirm(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    purhcases_repo: FromDishka[PurchasesRepo],
) -> None:
    pass
