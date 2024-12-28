from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.handlers.client.cart.states import CartStates
from bot.handlers.client.help.states import HelpStates
from bot.handlers.client.shop.states import ShopStates
from bot.handlers.client.transfer_funds.states import TransferFundsStates


async def on_shop(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=ShopStates.list)


async def on_cart(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=CartStates.cart)


async def on_transfer_funds(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=TransferFundsStates.id)


async def on_help(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=HelpStates.help)
