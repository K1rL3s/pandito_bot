from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from database.repos.secrets import SecretsRepo


@inject
async def get_all_secrets(
    dialog_manager: DialogManager,
    secrets_repo: FromDishka[SecretsRepo],
    **__: Any,
) -> dict[str, Any]:
    secrets = await secrets_repo.get_all()
    return {"secrets": secrets}


@inject
async def get_one_secret(
    dialog_manager: DialogManager,
    secrets_repo: FromDishka[SecretsRepo],
    **__: Any,
) -> dict[str, Any]:
    if "secret_id" in dialog_manager.dialog_data:
        secret_id: int = dialog_manager.dialog_data["secret_id"]
    else:
        secret_id: int = dialog_manager.start_data["secret_id"]
        dialog_manager.dialog_data["secret_id"] = secret_id

    secret = await secrets_repo.get_by_id(secret_id)
    total_activations = await secrets_repo.total_activations(secret_id)
    return {"secret": secret, "total_activations": total_activations}