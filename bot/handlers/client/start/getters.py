from typing import Any

from aiogram_dialog import DialogManager


async def full_name_getter(dialog_manager: DialogManager, **__: Any) -> dict[str, str]:
    return {"full_name": dialog_manager.dialog_data["full_name"]}
