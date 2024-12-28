from typing import Any

from aiogram import Router
from aiogram.fsm.state import State
from aiogram_dialog import AccessSettings, ShowMode, StartMode
from aiogram_dialog.api.entities import ChatEvent
from aiogram_dialog.api.internal import DialogManagerFactory
from aiogram_dialog.api.protocols import (
    DialogManager,
    DialogRegistryProtocol,
    MediaIdStorageProtocol,
    MessageManagerProtocol,
)
from aiogram_dialog.manager.manager import ManagerImpl


class CustomStartModeShowModeManagerImpl(ManagerImpl):
    async def start(
        self,
        state: State,
        data: dict[str, Any] | None = None,
        mode: StartMode = StartMode.RESET_STACK,
        show_mode: ShowMode | None = ShowMode.DELETE_AND_SEND,
        access_settings: AccessSettings | None = None,
    ) -> None:
        if data is None:
            data = {}

        self.check_disabled()
        self.show_mode = show_mode or self.show_mode
        if mode is StartMode.NORMAL:
            await self._start_normal(state, data, access_settings)
        elif mode is StartMode.RESET_STACK:
            await self.reset_stack(remove_keyboard=False)
            await self._start_normal(state, data, access_settings)
        elif mode is StartMode.NEW_STACK:
            await self._start_new_stack(state, data, access_settings)
        else:
            raise ValueError(f"Unknown start mode: {mode}")


class MyManagerFactory(DialogManagerFactory):
    def __init__(
        self,
        message_manager: MessageManagerProtocol,
        media_id_storage: MediaIdStorageProtocol,
    ) -> None:
        self.message_manager = message_manager
        self.media_id_storage = media_id_storage

    def __call__(
        self,
        event: ChatEvent,
        data: dict,
        registry: DialogRegistryProtocol,
        router: Router,
    ) -> DialogManager:
        return CustomStartModeShowModeManagerImpl(
            event=event,
            data=data,
            message_manager=self.message_manager,
            media_id_storage=self.media_id_storage,
            registry=registry,
            router=router,
        )
