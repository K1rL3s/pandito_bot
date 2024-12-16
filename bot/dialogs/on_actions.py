from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button

from bot.handlers.client.menu.states import MenuStates
from bot.handlers.client.products.states import ProductsStates
from database.models import UserModel


async def on_empty_button(
    callback: CallbackQuery,
    _: Button,
    __: DialogManager,
) -> None:
    await callback.answer("🤫🧏")


async def on_go_to_menu(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserModel = dialog_manager.middleware_data["user"]
    await dialog_manager.start(
        state=MenuStates.menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={"role": user.role},
    )


async def on_go_to_products(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserModel = dialog_manager.middleware_data["user"]
    await dialog_manager.start(
        state=ProductsStates.list,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={"user": user},
    )


async def on_go_back(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.back()
