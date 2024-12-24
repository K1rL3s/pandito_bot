from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.services.secrets import SecretsService
from database.repos.secrets import SecretsRepo

from .states import CreateSecretStates, ViewSecretsStates


async def on_secret_selected(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    dialog_manager.dialog_data["secret_id"] = item_id
    await dialog_manager.next()


async def on_create_secret(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=CreateSecretStates.phrase)


async def on_delete_secret(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.next()


@inject
async def on_confirm_delete_secret(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    secrets_repo: FromDishka[SecretsRepo],
) -> None:
    secret_id: int = dialog_manager.dialog_data["secret_id"]
    await secrets_repo.delete(secret_id)
    await dialog_manager.start(state=ViewSecretsStates.list)


async def secret_phrase_input(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    phrase = message.text.strip()
    dialog_manager.dialog_data["phrase"] = phrase
    await dialog_manager.next()


async def secret_reward_input(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    reward = int(message.text.strip())
    dialog_manager.dialog_data["reward"] = reward
    await dialog_manager.next()


async def secret_activation_limit_input(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    activation_limit = int(message.text.strip())
    dialog_manager.dialog_data["activation_limit"] = activation_limit
    await dialog_manager.next()


@inject
async def confirm_create_secret(
    callback: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    secrets_service: FromDishka[SecretsService],
) -> None:
    phrase: str = dialog_manager.dialog_data["phrase"]
    reward: int = dialog_manager.dialog_data["reward"]
    activation_limit: int = dialog_manager.dialog_data["activation_limit"]
    creator_id = callback.from_user.id
    secret_id = await secrets_service.create_secret(
        phrase,
        reward,
        activation_limit,
        creator_id,
    )

    dialog_manager.dialog_data["secret_id"] = secret_id
    await dialog_manager.start(
        state=ViewSecretsStates.one,
        data={"secret_id": secret_id},
    )
