from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.services.purchases import PurchasesService
from database.models import UserModel


@inject
async def on_clear_cart_confirm(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    purhcases_service: FromDishka[PurchasesService],
) -> None:
    view_user: UserModel = dialog_manager.dialog_data["view_user"]
    admin: UserModel = dialog_manager.middleware_data["user"]
    await purhcases_service.clear_cart(view_user.id, admin.id)
    await dialog_manager.next()
