from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button

from bot.handlers.client.cart.states import CartStates
from bot.handlers.client.help.states import HelpStates
from bot.handlers.client.shop.states import ShopStates
from database.models import UserModel


async def on_shop(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserModel = dialog_manager.middleware_data["user"]
    await dialog_manager.start(
        state=ShopStates.list,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={"user": user},
    )


async def on_cart(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=CartStates.cart,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_transfer_funds(  # TODO: переделать на трансфер
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserModel = dialog_manager.middleware_data["user"]
    await dialog_manager.start(
        state=ShopStates.list,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={"user": user},
    )


async def on_help(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=HelpStates.help,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
