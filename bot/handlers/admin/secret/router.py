from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from dishka import FromDishka

from core.services.secrets import SecretsService
from database.repos.secrets import SecretsRepo

router = Router(name=__file__)


@router.message(Command("list_secrets"), StateFilter(None))
async def list_secrets_handler(
    message: Message,
    secrets_repo: FromDishka[SecretsRepo],
) -> None:
    secrets = await secrets_repo.get_all()

    text = "\n".join(
        [f"{secret.id} | <code>{secret.phrase}</code>" for secret in secrets],
    )
    await message.answer(text=text)


@router.message(Command("create_secret"), StateFilter(None))
async def create_secret_handler(
    message: Message,
    command: CommandObject,
    secrets_service: FromDishka[SecretsService],
) -> None:
    reward, secret_phrase = command.args.split(maxsplit=1)
    secret_id = await secrets_service.create_secret(
        secret_phrase,
        int(reward),
        message.from_user.id,
    )

    text = f"Успех! id: {secret_id}"
    await message.answer(text=text)


@router.message(Command("delete_secret"), StateFilter(None))
async def delete_secret_handler(
    message: Message,
    command: CommandObject,
    secrets_repo: FromDishka[SecretsRepo],
) -> None:
    if command.args and len(command.args.split()) == 1:
        secret_id = int(command.args)
        await secrets_repo.delete(secret_id)
        await message.answer(f"Секрет с ID {secret_id} был успешно удален.")
    else:
        await message.answer("Формат: /delete_secret <id>", parse_mode=None)
