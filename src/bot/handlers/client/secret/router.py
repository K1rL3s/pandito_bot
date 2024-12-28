from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka

from bot.enums import SlashCommand
from core.services.secrets import SecretsService

router = Router(name=__file__)


@router.message(Command(SlashCommand.SECRET))
async def check_secret_handler(
    message: Message,
    command: CommandObject,
    secrets_service: FromDishka[SecretsService],
) -> None:
    if secret_phrase := command.args.strip():
        reward = await secrets_service.reward_for_secret(
            message.from_user.id,
            secret_phrase,
        )
        if reward is not None:
            await message.answer(f"🕵 Секрет найден! Начислено {reward} коинов 💰")

    await message.delete()
