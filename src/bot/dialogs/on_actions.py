from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def on_start_update_dialog_data(_: Any, dialog_manager: DialogManager) -> None:
    if isinstance(dialog_manager.start_data, dict):
        dialog_manager.dialog_data.update(dialog_manager.start_data)


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
    from bot.handlers.client.menu.states import MenuStates

    await dialog_manager.start(state=MenuStates.menu)


async def on_go_to_admin_panel(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    from bot.handlers.admin.panel.states import AdminPanelStates

    await dialog_manager.start(state=AdminPanelStates.panel)


async def on_go_to_products(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    from bot.handlers.client.shop.states import ShopStates

    await dialog_manager.start(state=ShopStates.list)
